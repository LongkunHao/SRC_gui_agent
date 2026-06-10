#!/usr/bin/env bash
# Stop or terminate pipeline EC2 instances. EIPs return to the pool for reuse.
#
# Finds all instances tagged Project=mirror-mirror and stops them (default)
# or terminates them. Stopped instances preserve EBS volumes and can be
# restarted for debugging.
#
# Usage:
#   bash infra/setup/teardown.sh                   # stop instances (EIPs return to pool, EBS preserved)
#   bash infra/setup/teardown.sh --terminate       # terminate instances (EBS deleted)
#   bash infra/setup/teardown.sh --release-eips    # stop + release EIPs (destroys Claude auth)
#   bash infra/setup/teardown.sh --all             # terminate + release EIPs + delete SG + IAM role

set -euo pipefail

# --- Load central config ---
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$REPO_ROOT/infra/config.sh"

REGION="$MM_REGION"
RELEASE_EIPS=false
DELETE_ALL=false
TERMINATE=false

for arg in "$@"; do
  case "$arg" in
    --terminate)    TERMINATE=true ;;
    --release-eips) RELEASE_EIPS=true ;;
    --all)          DELETE_ALL=true; RELEASE_EIPS=true; TERMINATE=true ;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

# --- Stop or terminate instances ---
if $TERMINATE; then
  echo "=== Terminating mirror-mirror EC2 instances ==="
else
  echo "=== Stopping mirror-mirror EC2 instances ==="
fi

INSTANCE_IDS=$(aws ec2 describe-instances \
  --filters "Name=tag:Project,Values=${MM_PROJECT_TAG}" "Name=instance-state-name,Values=pending,running,stopping,stopped" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text --region "$REGION")

if [ -n "$INSTANCE_IDS" ]; then
  for id in $INSTANCE_IDS; do
    ENV_ID=$(aws ec2 describe-instances --instance-ids "$id" \
      --query 'Reservations[0].Instances[0].Tags[?Key==`EnvId`].Value | [0]' --output text --region "$REGION")
    STATE=$(aws ec2 describe-instances --instance-ids "$id" \
      --query 'Reservations[0].Instances[0].State.Name' --output text --region "$REGION")
    echo "  $id  ${ENV_ID:-unknown}  ($STATE)"
  done

  if $TERMINATE; then
    echo "  Terminating..."
    aws ec2 terminate-instances --instance-ids $INSTANCE_IDS --region "$REGION" > /dev/null
    echo "  Waiting for termination..."
    aws ec2 wait instance-terminated --instance-ids $INSTANCE_IDS --region "$REGION"
  else
    # Only stop running instances (already-stopped ones are fine)
    RUNNING_IDS=$(aws ec2 describe-instances \
      --instance-ids $INSTANCE_IDS \
      --filters "Name=instance-state-name,Values=pending,running" \
      --query 'Reservations[].Instances[].InstanceId' \
      --output text --region "$REGION")
    if [ -n "$RUNNING_IDS" ]; then
      echo "  Stopping..."
      aws ec2 stop-instances --instance-ids $RUNNING_IDS --region "$REGION" > /dev/null
      echo "  Waiting for instances to stop..."
      aws ec2 wait instance-stopped --instance-ids $RUNNING_IDS --region "$REGION"
    else
      echo "  All instances already stopped."
    fi
  fi
  echo "  Done."
else
  echo "  No instances found."
fi

# --- Disassociate Elastic IPs (return to pool) ---
echo ""
EIP_JSON=$(aws ec2 describe-addresses \
  --filters "Name=tag:Project,Values=${MM_PROJECT_TAG}" \
  --query 'Addresses[].[AllocationId,PublicIp,AssociationId]' \
  --output json --region "$REGION" 2>/dev/null || echo "[]")
EIP_COUNT=$(echo "$EIP_JSON" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")

if [ "$EIP_COUNT" -gt 0 ]; then
  if $RELEASE_EIPS; then
    echo "=== Releasing Elastic IPs (WARNING: Claude auth sessions will be lost) ==="
  else
    echo "=== Returning Elastic IPs to pool ==="
  fi

  echo "$EIP_JSON" | python3 -c "
import sys, json
for alloc_id, ip, assoc_id in json.load(sys.stdin):
    print(f'{alloc_id} {ip} {assoc_id or \"none\"}')
" | while read -r ALLOC_ID IP ASSOC_ID; do
    if [ "$ASSOC_ID" != "none" ]; then
      aws ec2 disassociate-address --association-id "$ASSOC_ID" --region "$REGION" 2>/dev/null
      echo "  Disassociated: $IP ($ALLOC_ID)"
    fi
    if $RELEASE_EIPS; then
      aws ec2 release-address --allocation-id "$ALLOC_ID" --region "$REGION" 2>/dev/null && \
        echo "  Released: $IP ($ALLOC_ID)" || echo "  Failed to release: $ALLOC_ID"
    fi
  done

  if ! $RELEASE_EIPS; then
    echo "  $EIP_COUNT EIP(s) retained in pool (use --release-eips to destroy)"
  fi
else
  echo "=== No Elastic IPs found ==="
fi

# --- Full cleanup ---
if $DELETE_ALL; then
  echo ""
  echo "=== Deleting security group ==="
  SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$MM_SECURITY_GROUP" \
    --query 'SecurityGroups[0].GroupId' --output text --region "$REGION" 2>/dev/null || true)
  if [ -n "$SG_ID" ] && [ "$SG_ID" != "None" ]; then
    aws ec2 delete-security-group --group-id "$SG_ID" --region "$REGION" 2>/dev/null && \
      echo "  Deleted: $SG_ID" || echo "  Failed (may have dependencies): $SG_ID"
  else
    echo "  No $MM_SECURITY_GROUP security group found."
  fi

  echo ""
  echo "=== Deleting IAM role ==="
  ROLE_NAME="$MM_IAM_ROLE"
  aws iam remove-role-from-instance-profile --instance-profile-name "$ROLE_NAME" --role-name "$ROLE_NAME" 2>/dev/null || true
  aws iam delete-instance-profile --instance-profile-name "$ROLE_NAME" 2>/dev/null || true
  aws iam detach-role-policy --role-name "$ROLE_NAME" --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess 2>/dev/null || true
  aws iam delete-role --role-name "$ROLE_NAME" 2>/dev/null && echo "  Deleted role: $ROLE_NAME" || echo "  No role found."
fi

if ! $DELETE_ALL; then
  echo ""
  if $TERMINATE; then
    echo "Instances terminated. Security group, IAM role, and EIP pool preserved."
  else
    echo "Instances stopped (EBS preserved). Restart with: aws ec2 start-instances --instance-ids ..."
  fi
  echo "To delete everything: bash infra/setup/teardown.sh --all"
fi

echo ""
echo "=== Teardown complete ==="
