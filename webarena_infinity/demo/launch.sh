#!/usr/bin/env bash
# Launch a single EC2 instance for the Mirror-Mirror demo server.
#
# Prerequisites:
#   - AWS CLI configured
#   - KEY_PAIR_NAME env var set (or pass --key-pair)
#   - GITHUB_TOKEN and GITHUB_REPO env vars set (for git clone)
#
# Usage:
#   bash infra/demo/launch.sh
#   bash infra/demo/launch.sh --instance-type t3a.large --key-pair my-key

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
set -a && source "$REPO_ROOT/.env" 2>/dev/null && set +a
source "$REPO_ROOT/infra/config.sh"

# --- Defaults ---
INSTANCE_TYPE="${MM_DEMO_INSTANCE_TYPE:-t3a.large}"
KEY_PAIR="${KEY_PAIR_NAME:-}"
REGION="$MM_REGION"
SG_NAME="mm-demo"
BASE_PORT=9000
# Total number of app ports to open (generous upper bound)
NUM_APP_PORTS=25
LAUNCH_FILE="/tmp/mirror-mirror-demo.env"

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --instance-type)  INSTANCE_TYPE="$2";  shift 2 ;;
    --key-pair)       KEY_PAIR="$2";       shift 2 ;;
    --region)         REGION="$2";         shift 2 ;;
    --launch-file)    LAUNCH_FILE="$2";    shift 2 ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

# --- Validate ---
for var in GITHUB_TOKEN GITHUB_REPO KEY_PAIR; do
  val="${!var:-}"
  if [ -z "$val" ]; then
    echo "ERROR: $var is not set."
    echo "  Required: GITHUB_TOKEN, GITHUB_REPO, KEY_PAIR_NAME"
    exit 1
  fi
done

echo "=== Mirror-Mirror Demo Launch ==="
echo "  Instance type:   $INSTANCE_TYPE"
echo "  Region:          $REGION"
echo "  Key pair:        $KEY_PAIR"
echo ""

# --- Resolve AMI (Amazon Linux 2023) ---
AMI_ID=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" \
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
  --output text --region "$REGION")
echo "  AMI:             $AMI_ID"

# --- Security group (create if needed) ---
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' --output text --region "$REGION")

SG_ID=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=$SG_NAME" "Name=vpc-id,Values=$VPC_ID" \
  --query 'SecurityGroups[0].GroupId' --output text --region "$REGION" 2>/dev/null || true)

if [ -z "$SG_ID" ] || [ "$SG_ID" = "None" ]; then
  echo "  Creating security group: $SG_NAME"
  SG_ID=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "Mirror-Mirror demo (SSH + HTTP + app ports)" \
    --vpc-id "$VPC_ID" \
    --query 'GroupId' --output text --region "$REGION")

  # SSH
  aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 \
    --region "$REGION" > /dev/null

  # HTTP (nginx)
  aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" --protocol tcp --port 80 --cidr 0.0.0.0/0 \
    --region "$REGION" > /dev/null

  # App ports (9000-9025)
  LAST_PORT=$((BASE_PORT + NUM_APP_PORTS))
  aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" --protocol tcp --port "${BASE_PORT}-${LAST_PORT}" --cidr 0.0.0.0/0 \
    --region "$REGION" > /dev/null

  echo "  Created: $SG_ID"
else
  echo "  Reusing security group: $SG_ID"
fi

# --- Subnet ---
SUBNET_ID=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=default-for-az,Values=true" \
  --query 'Subnets[0].SubnetId' --output text --region "$REGION")

# --- User data (setup script) ---
USERDATA=$(cat <<'SETUP_EOF'
#!/bin/bash
set -uo pipefail
exec > /var/log/mirror-mirror-demo-setup.log 2>&1

export HOME=/home/ec2-user
cd $HOME

echo "=== Installing system packages ==="
dnf update -y
dnf install -y git python3.12 python3.12-pip nginx

echo "=== Installing Python packages ==="
python3.12 -m pip install requests

echo "=== Cloning repository ==="
for attempt in 1 2 3; do
  su - ec2-user -c 'git clone https://GITHUB_TOKEN_PLACEHOLDER@github.com/GITHUB_REPO_PLACEHOLDER.git /home/ec2-user/mirror-mirror' && break
  echo "Clone attempt $attempt failed, retrying..."
  rm -rf /home/ec2-user/mirror-mirror
  sleep 10
done

if [ ! -d /home/ec2-user/mirror-mirror/.git ]; then
  echo "FATAL: git clone failed"
  exit 1
fi

echo "=== Configuring nginx ==="
# Write a minimal nginx.conf that only includes our proxy config
cat > /etc/nginx/nginx.conf <<'NGINX_MAIN'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent"';
    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    include /etc/nginx/conf.d/*.conf;
}
NGINX_MAIN

cp /home/ec2-user/mirror-mirror/infra/demo/nginx.conf /etc/nginx/conf.d/mirror-mirror.conf
rm -f /etc/nginx/conf.d/default.conf

nginx -t && systemctl enable nginx && systemctl start nginx

echo "=== Starting demo server ==="
cat > /etc/systemd/system/mirror-mirror-demo.service <<'SERVICE'
[Unit]
Description=Mirror-Mirror Demo Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/mirror-mirror
ExecStart=/usr/bin/python3.12 serve_all.py --demo --host 0.0.0.0 --port 9000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable mirror-mirror-demo
systemctl start mirror-mirror-demo

touch /home/ec2-user/.setup-complete
echo ""
echo "======================================"
echo "Demo setup complete!"
echo "======================================"
SETUP_EOF
)

# Substitute actual tokens into user data
USERDATA="${USERDATA//GITHUB_TOKEN_PLACEHOLDER/$GITHUB_TOKEN}"
USERDATA="${USERDATA//GITHUB_REPO_PLACEHOLDER/$GITHUB_REPO}"

# --- Launch instance ---
echo ""
echo "=== Launching instance ==="
INST_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_PAIR" \
  --subnet-id "$SUBNET_ID" \
  --security-group-ids "$SG_ID" \
  --associate-public-ip-address \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30}}]' \
  --user-data "$USERDATA" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=mm-demo},{Key=Project,Value=${MM_PROJECT_TAG}},{Key=Role,Value=demo}]" \
  --query 'Instances[0].InstanceId' --output text --region "$REGION")

echo "  Instance: $INST_ID"
echo "  Waiting for running state..."
aws ec2 wait instance-running --instance-ids "$INST_ID" --region "$REGION"

# --- Allocate Elastic IP ---
echo ""
echo "=== Assigning Elastic IP ==="
EIP_JSON=$(aws ec2 allocate-address --domain vpc \
  --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=mm-demo},{Key=Project,Value=${MM_PROJECT_TAG}},{Key=Role,Value=demo}]" \
  --region "$REGION")
ALLOC_ID=$(echo "$EIP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['AllocationId'])")
PUBLIC_IP=$(echo "$EIP_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['PublicIp'])")

aws ec2 associate-address --instance-id "$INST_ID" --allocation-id "$ALLOC_ID" \
  --region "$REGION" > /dev/null

echo "  Elastic IP: $PUBLIC_IP"

# --- Save launch info ---
cat > "$LAUNCH_FILE" <<EOF
# Mirror-Mirror Demo — $(date -u +%Y-%m-%dT%H:%M:%SZ)
INSTANCE_ID="$INST_ID"
PUBLIC_IP="$PUBLIC_IP"
EIP_ALLOC_ID="$ALLOC_ID"
INSTANCE_TYPE="$INSTANCE_TYPE"
REGION="$REGION"
KEY_PAIR="$KEY_PAIR"
SG_ID="$SG_ID"
EOF

echo ""
echo "=== Launch Complete ==="
echo ""
echo "  Instance:    $INST_ID"
echo "  Public IP:   $PUBLIC_IP"
echo "  Homepage:    http://$PUBLIC_IP"
echo ""
echo "  Setup takes ~3-5 minutes. Monitor with:"
echo "    ssh -i ~/.ssh/${KEY_PAIR}.pem ec2-user@${PUBLIC_IP} tail -f /var/log/mirror-mirror-demo-setup.log"
echo ""
echo "  Launch info saved to: $LAUNCH_FILE"
echo ""
echo "  Teardown:"
echo "    bash infra/demo/teardown.sh"
