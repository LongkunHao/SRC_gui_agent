#!/usr/bin/env bash
# Launch EC2 instance(s) for running eval across all apps.
#
# Uses the pre-built AMI with ~/venv already set up (no setup.sh needed).
# Clones main branch, sets API keys, installs vision agent deps.
#
# Prerequisites:
#   Set these env vars (or source .env):
#     GITHUB_TOKEN       — for git clone
#     GITHUB_REPO        — GitHub owner/repo (e.g. myuser/mirror-mirror)
#     GOOGLE_API_KEY     — for Gemini agents
#     ANTHROPIC_API_KEY  — for Claude agents
#     KIMI_API_KEY       — for Kimi agent
#     KEY_PAIR_NAME      — EC2 key pair name
#
# Usage:
#   # Launch one instance
#   bash infra/setup/launch_eval.sh
#
#   # Launch 4 instances (one per model)
#   bash infra/setup/launch_eval.sh --count 4
#
#   # Custom instance type or AMI
#   bash infra/setup/launch_eval.sh --instance-type m5.2xlarge --ami ami-0abc123
#
# After launch, SSH in and run:
#   source ~/.bashrc
#   cd ~/mirror-mirror
#   nohup bash infra/run_all_apps.sh --model gemini-flash --workers 8 \
#     > /tmp/mirror-mirror-logs/eval.log 2>&1 &

set -euo pipefail

# --- Load .env and central config ---
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [ -f "$REPO_ROOT/.env" ]; then
    set -a && source "$REPO_ROOT/.env" && set +a
fi
source "$REPO_ROOT/infra/config.sh"

# --- Defaults ---
INSTANCE_TYPE="$MM_INSTANCE_TYPE"
KEY_PAIR="${KEY_PAIR_NAME:-}"
REGION="$MM_REGION"
AMI=""
COUNT=1
SG_ID=""
SUBNET_ID=""

# --- Parse args ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --instance-type) INSTANCE_TYPE="$2"; shift 2 ;;
        --ami)           AMI="$2";           shift 2 ;;
        --count)         COUNT="$2";         shift 2 ;;
        --key-pair)      KEY_PAIR="$2";      shift 2 ;;
        --region)        REGION="$2";        shift 2 ;;
        --security-group) SG_ID="$2";        shift 2 ;;
        --subnet)        SUBNET_ID="$2";     shift 2 ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# --- Validate ---
for var in GITHUB_TOKEN GITHUB_REPO KEY_PAIR AMI; do
    if [ -z "${!var:-}" ]; then
        echo "ERROR: $var is not set."
        echo "  Pass --ami <ami-id> or set BASE_AMI env var."
        echo "  Create a base AMI with: bash infra/setup/create_base_ami.sh"
        exit 1
    fi
done

# --- Resolve SG and subnet ---
if [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 describe-security-groups \
        --filters "Name=group-name,Values=$MM_SECURITY_GROUP" \
        --query 'SecurityGroups[0].GroupId' --output text --region "$REGION")
fi
if [ -z "$SUBNET_ID" ]; then
    VPC_ID=$(aws ec2 describe-security-groups --group-ids "$SG_ID" \
        --query 'SecurityGroups[0].VpcId' --output text --region "$REGION")
    SUBNET_ID=$(aws ec2 describe-subnets \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=default-for-az,Values=true" \
        --query 'Subnets[0].SubnetId' --output text --region "$REGION")
fi

echo "=== Eval Instance Launch ==="
echo "  AMI:           $AMI"
echo "  Instance type: $INSTANCE_TYPE"
echo "  Count:         $COUNT"
echo "  Region:        $REGION"
echo ""

# --- Build user-data ---
USERDATA=$(cat <<EOF
#!/bin/bash
set -uo pipefail
exec > /var/log/mirror-mirror-setup.log 2>&1
export HOME=/home/ec2-user
cd \$HOME
rm -f /home/ec2-user/.setup-complete

for attempt in 1 2 3; do
  su - ec2-user -c 'git clone --branch main https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git /home/ec2-user/mirror-mirror' && break
  echo "Clone attempt \$attempt failed, retrying in 10s..."
  rm -rf /home/ec2-user/mirror-mirror
  sleep 10
done

cat >> /home/ec2-user/.bashrc <<'ENVVARS'
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
export KIMI_API_KEY="${KIMI_API_KEY:-}"
ENVVARS

# Install vision agent deps into AMI's existing venv
su - ec2-user -c 'source ~/venv/bin/activate && pip install google-genai openai'

mkdir -p /tmp/mirror-mirror-logs
chown ec2-user:ec2-user /tmp/mirror-mirror-logs
touch /home/ec2-user/.setup-complete
echo "Setup complete — ready for eval"
EOF
)

# --- Launch instances ---
for i in $(seq 1 "$COUNT"); do
    INST_ID=$(aws ec2 run-instances \
        --image-id "$AMI" \
        --instance-type "$INSTANCE_TYPE" \
        --key-name "$KEY_PAIR" \
        --subnet-id "$SUBNET_ID" \
        --security-group-ids "$SG_ID" \
        --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":50}}]' \
        --user-data "$USERDATA" \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=mm-eval-${i}},{Key=Project,Value=${MM_PROJECT_TAG}},{Key=Role,Value=eval}]" \
        --query 'Instances[0].InstanceId' --output text --region "$REGION")

    echo "  Instance $i: $INST_ID (waiting for running...)"
    aws ec2 wait instance-running --instance-ids "$INST_ID" --region "$REGION"

    # Allocate and assign EIP
    EIP_JSON=$(aws ec2 allocate-address --domain vpc \
        --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=mm-eip-eval-${i}},{Key=Project,Value=${MM_PROJECT_TAG}}]" \
        --region "$REGION")
    ALLOC_ID=$(echo "$EIP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['AllocationId'])")
    EIP=$(echo "$EIP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['PublicIp'])")
    aws ec2 associate-address --instance-id "$INST_ID" --allocation-id "$ALLOC_ID" --region "$REGION" > /dev/null

    echo "  Instance $i: $INST_ID → $EIP"
    echo "    ssh -i ~/.ssh/mirror-mirror.pem ec2-user@$EIP"
    echo ""
done

echo "=== All $COUNT instance(s) launched ==="
echo ""
echo "After SSH, run:"
echo "  source ~/.bashrc && cd ~/mirror-mirror"
echo "  nohup bash infra/run_all_apps.sh --model <MODEL> --workers 8 \\"
echo "    > /tmp/mirror-mirror-logs/eval.log 2>&1 &"
echo ""
echo "Tear down with:"
echo "  bash infra/setup/teardown.sh"
