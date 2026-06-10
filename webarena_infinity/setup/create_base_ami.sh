#!/usr/bin/env bash
# Create a golden AMI with all dependencies pre-installed.
#
# This launches a single EC2 instance, installs system packages, Python,
# Node.js, Claude CLI, Playwright + Chromium, and Python deps. You then
# SSH in to run `claude login` and `claude plugins install frontend-design`.
# Once done, the script creates an AMI from the instance.
#
# Usage:
#   bash infra/setup/create_base_ami.sh
#   bash infra/setup/create_base_ami.sh --instance-type m5.xlarge --region us-east-1

set -euo pipefail

# --- Load central config ---
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$REPO_ROOT/infra/config.sh"

# --- Defaults ---
INSTANCE_TYPE="$MM_INSTANCE_TYPE"
KEY_PAIR="${KEY_PAIR_NAME:-}"
REGION="$MM_REGION"
SG_ID=""
SUBNET_ID=""
AMI_NAME_PREFIX="mm-base"

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --instance-type)  INSTANCE_TYPE="$2";  shift 2 ;;
    --key-pair)       KEY_PAIR="$2";       shift 2 ;;
    --region)         REGION="$2";         shift 2 ;;
    --security-group) SG_ID="$2";          shift 2 ;;
    --subnet)         SUBNET_ID="$2";      shift 2 ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: bash infra/setup/create_base_ami.sh [OPTIONS]"
      exit 1
      ;;
  esac
done

# --- Validate ---
if [ -z "$KEY_PAIR" ]; then
  echo "ERROR: KEY_PAIR_NAME is not set. Set it or pass --key-pair."
  exit 1
fi

echo "=== Base AMI Creation ==="
echo "  Instance type: $INSTANCE_TYPE"
echo "  Key pair:      $KEY_PAIR"
echo "  Region:        $REGION"
echo ""

# --- Find latest Amazon Linux 2023 AMI ---
AL2023_AMI=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" \
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
  --output text --region "$REGION")
echo "  Base AMI: $AL2023_AMI"

# --- Security group ---
if [ -z "$SG_ID" ]; then
  VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
    --query 'Vpcs[0].VpcId' --output text --region "$REGION" 2>/dev/null || true)
  if [ -z "$VPC_ID" ] || [ "$VPC_ID" = "None" ]; then
    echo "No default VPC found. Provide --security-group and --subnet manually."
    exit 1
  fi
  SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$MM_SECURITY_GROUP" "Name=vpc-id,Values=$VPC_ID" \
    --query 'SecurityGroups[0].GroupId' --output text --region "$REGION" 2>/dev/null || true)
  if [ -z "$SG_ID" ] || [ "$SG_ID" = "None" ]; then
    echo "Creating security group: $MM_SECURITY_GROUP"
    SG_ID=$(aws ec2 create-security-group \
      --group-name "$MM_SECURITY_GROUP" \
      --description "Mirror-Mirror pipeline (SSH only)" \
      --vpc-id "$VPC_ID" \
      --query 'GroupId' --output text --region "$REGION")
    aws ec2 authorize-security-group-ingress \
      --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 \
      --region "$REGION" > /dev/null
  fi
  echo "  Security group: $SG_ID"
fi

# --- Subnet ---
if [ -z "$SUBNET_ID" ]; then
  VPC_ID=$(aws ec2 describe-security-groups --group-ids "$SG_ID" \
    --query 'SecurityGroups[0].VpcId' --output text --region "$REGION")
  SUBNET_ID=$(aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=default-for-az,Values=true" \
    --query 'Subnets[0].SubnetId' --output text --region "$REGION")
  echo "  Subnet: $SUBNET_ID"
fi

# --- User-data: install everything except env-specific config ---
USERDATA=$(cat <<'SETUP_EOF'
#!/bin/bash
set -uo pipefail
exec > /var/log/mirror-mirror-setup.log 2>&1

export HOME=/home/ec2-user
cd $HOME

# System packages
dnf update -y
dnf install -y git gcc gcc-c++ make openssl-devel bzip2-devel \
  libffi-devel zlib-devel readline-devel sqlite-devel tmux

# Chromium dependencies
dnf install -y alsa-lib atk at-spi2-atk cups-libs libdrm mesa-libgbm \
  pango libXcomposite libXdamage libXrandr libxkbcommon nss nspr

# Python via uv
su - ec2-user -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
su - ec2-user -c 'export PATH="$HOME/.local/bin:$PATH" && uv python install 3.12'

# Create venv
su - ec2-user -c 'export PATH="$HOME/.local/bin:$PATH" && uv venv $HOME/venv --python 3.12'
echo 'export PATH="$HOME/venv/bin:$HOME/.local/bin:$PATH"' >> /home/ec2-user/.bashrc

# Node.js 20
curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
dnf install -y nodejs

# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Python deps
su - ec2-user -c 'export PATH="$HOME/.local/bin:$PATH" && VIRTUAL_ENV=$HOME/venv uv pip install playwright "browser-use>=0.11.9" requests python-dotenv'

# Playwright + Chromium
su - ec2-user -c '$HOME/venv/bin/python -m playwright install chromium'
$HOME/venv/bin/python -m playwright install-deps || true

# Git config
su - ec2-user -c 'git config --global user.email "mirror-mirror-bot@example.com"'
su - ec2-user -c 'git config --global user.name "mirror-mirror-bot"'

# Create logs directory
mkdir -p /tmp/mirror-mirror-logs
chown ec2-user:ec2-user /tmp/mirror-mirror-logs

# Signal setup complete
touch /home/ec2-user/.setup-complete
echo ""
echo "======================================"
echo "Base setup complete!"
echo "======================================"
echo "Next steps (manual):"
echo "  1. claude login"
echo "  2. claude plugins install frontend-design"
echo "  3. Signal back to create AMI"
SETUP_EOF
)

# --- Launch instance ---
echo ""
echo "=== Launching template instance ==="
INST_ID=$(aws ec2 run-instances \
  --image-id "$AL2023_AMI" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_PAIR" \
  --subnet-id "$SUBNET_ID" \
  --security-group-ids "$SG_ID" \
  --associate-public-ip-address \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":50}}]' \
  --user-data "$USERDATA" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=mm-base-template},{Key=Project,Value=${MM_PROJECT_TAG}},{Key=Role,Value=base-template}]" \
  --query 'Instances[0].InstanceId' --output text --region "$REGION")

echo "  Instance: $INST_ID"
echo "  Waiting for running state..."
aws ec2 wait instance-running --instance-ids "$INST_ID" --region "$REGION"

PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INST_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text --region "$REGION")

echo ""
echo "=== Template instance is running ==="
echo "  Instance: $INST_ID"
echo "  IP:       $PUBLIC_IP"
echo ""
echo "=== MANUAL STEPS REQUIRED ==="
echo ""
echo "1. SSH into the instance:"
echo "   ssh -i ~/.ssh/${KEY_PAIR}.pem ec2-user@${PUBLIC_IP}"
echo ""
echo "2. Wait for setup to complete:"
echo "   tail -f /var/log/mirror-mirror-setup.log"
echo "   # (wait until you see 'Base setup complete!')"
echo ""
echo "3. Login to Claude and install plugins:"
echo "   claude login"
echo "   claude plugins install frontend-design"
echo ""
echo "4. Exit SSH and press Enter here to create the AMI."
echo ""
read -rp "Press Enter when ready to create AMI (or Ctrl+C to abort)..."

# Pre-accept --dangerously-skip-permissions trust dialog so pipeline runs non-interactively
echo ""
echo "=== Pre-accepting --dangerously-skip-permissions trust dialog ==="
ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
  "ec2-user@${PUBLIC_IP}" \
  "python3 -c \"
import json
with open('/home/ec2-user/.claude.json', 'r+') as f:
    d = json.load(f)
    for p in ['/home/ec2-user', '/home/ec2-user/mirror-mirror']:
        d.setdefault('projects', {}).setdefault(p, {})['hasTrustDialogAccepted'] = True
    f.seek(0); json.dump(d, f, indent=2); f.truncate()
print('Done: hasTrustDialogAccepted set for both project paths')
\""

# Ensure ~/.claude/settings.json has skipDangerousModePermissionPrompt
echo "=== Setting skipDangerousModePermissionPrompt in settings.json ==="
ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
  "ec2-user@${PUBLIC_IP}" \
  "python3 -c \"
import json, os
p = os.path.expanduser('~/.claude/settings.json')
d = {}
if os.path.exists(p):
    with open(p) as f: d = json.load(f)
d['skipDangerousModePermissionPrompt'] = True
with open(p, 'w') as f: json.dump(d, f, indent=2)
print('Done: skipDangerousModePermissionPrompt set')
\""

# --- Delete previous base AMI ---
echo ""
echo "=== Checking for previous base AMI ==="
OLD_AMI_ID=$(aws ec2 describe-images \
  --owners self \
  --filters "Name=name,Values=${AMI_NAME_PREFIX}-*" "Name=state,Values=available" \
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
  --output text --region "$REGION" 2>/dev/null || true)

if [ -n "$OLD_AMI_ID" ] && [ "$OLD_AMI_ID" != "None" ]; then
  OLD_AMI_NAME=$(aws ec2 describe-images --image-ids "$OLD_AMI_ID" \
    --query 'Images[0].Name' --output text --region "$REGION")
  echo "  Found previous AMI: $OLD_AMI_ID ($OLD_AMI_NAME)"

  # Get associated snapshots before deregistering
  OLD_SNAP_IDS=$(aws ec2 describe-images --image-ids "$OLD_AMI_ID" \
    --query 'Images[0].BlockDeviceMappings[*].Ebs.SnapshotId' \
    --output text --region "$REGION")

  echo "  Deregistering old AMI..."
  aws ec2 deregister-image --image-id "$OLD_AMI_ID" --region "$REGION"

  for SNAP_ID in $OLD_SNAP_IDS; do
    if [ -n "$SNAP_ID" ] && [ "$SNAP_ID" != "None" ]; then
      echo "  Deleting snapshot: $SNAP_ID"
      aws ec2 delete-snapshot --snapshot-id "$SNAP_ID" --region "$REGION" || true
    fi
  done
  echo "  Old AMI cleaned up."
else
  echo "  No previous base AMI found."
fi

# --- Create AMI ---
AMI_NAME="${AMI_NAME_PREFIX}-$(date -u +%Y%m%d-%H%M%S)"
echo ""
echo "=== Creating AMI: $AMI_NAME ==="
echo "  (This may take several minutes...)"

AMI_ID=$(aws ec2 create-image \
  --instance-id "$INST_ID" \
  --name "$AMI_NAME" \
  --description "Mirror-Mirror base image with Claude CLI, Playwright, Python 3.12, Node 20" \
  --tag-specifications "ResourceType=image,Tags=[{Key=Name,Value=${AMI_NAME}},{Key=Project,Value=${MM_PROJECT_TAG}}]" \
  --query 'ImageId' --output text --region "$REGION")

echo "  AMI ID: $AMI_ID"
echo "  Waiting for AMI to become available..."
aws ec2 wait image-available --image-ids "$AMI_ID" --region "$REGION"

echo ""
echo "=== AMI Ready ==="
echo "  AMI ID:   $AMI_ID"
echo "  AMI Name: $AMI_NAME"
echo ""

# # --- Smoke test: verify Claude CLI works ---
# echo "=== Smoke-testing Claude CLI on instance ==="
# SMOKE_OUTPUT=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=10 \
#   "ec2-user@${PUBLIC_IP}" \
#   "timeout 60 claude --dangerously-skip-permissions -p 'Reply with exactly: hello' --max-turns 1 2>&1" || true)

# echo "  Claude output: $SMOKE_OUTPUT"
# if echo "$SMOKE_OUTPUT" | grep -qi "hello"; then
#   echo "  Claude CLI smoke test PASSED"
# else
#   echo "  WARNING: Claude CLI smoke test FAILED — CLI may need re-authentication"
#   echo "  You may want to SSH in and run 'claude login' before using this AMI."
# fi
# echo ""

# --- Terminate template instance ---
read -rp "Terminate template instance $INST_ID? [Y/n] " CONFIRM
CONFIRM="${CONFIRM:-Y}"
if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
  aws ec2 terminate-instances --instance-ids "$INST_ID" --region "$REGION" > /dev/null
  echo "  Template instance terminated."
else
  echo "  Template instance kept running: $INST_ID ($PUBLIC_IP)"
fi

echo ""
echo "=== Done ==="
echo "Use this AMI with launch.sh:"
echo "  bash infra/setup/launch.sh --manifest infra/env_manifest.jsonl --ami $AMI_ID --model gemini-pro"
