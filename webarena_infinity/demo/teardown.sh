#!/usr/bin/env bash
# Tear down the Mirror-Mirror demo instance.
#
# Usage:
#   bash infra/demo/teardown.sh
#   bash infra/demo/teardown.sh --keep-eip     # keep the Elastic IP for reuse

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$REPO_ROOT/infra/config.sh"

REGION="$MM_REGION"
RELEASE_EIP=true
LAUNCH_FILE="/tmp/mirror-mirror-demo.env"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep-eip)      RELEASE_EIP=false; shift ;;
    --region)        REGION="$2";       shift 2 ;;
    --launch-file)   LAUNCH_FILE="$2";  shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Find demo instances by tag
INST_IDS=$(aws ec2 describe-instances \
  --filters "Name=tag:Project,Values=${MM_PROJECT_TAG}" \
            "Name=tag:Role,Values=demo" \
            "Name=instance-state-name,Values=running,stopped,pending" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text --region "$REGION" 2>/dev/null || true)

if [ -z "$INST_IDS" ]; then
  echo "No demo instances found."
else
  echo "Terminating demo instance(s): $INST_IDS"
  aws ec2 terminate-instances --instance-ids $INST_IDS --region "$REGION" > /dev/null
  echo "  Waiting for termination..."
  aws ec2 wait instance-terminated --instance-ids $INST_IDS --region "$REGION"
  echo "  Done."
fi

# Release EIPs
if $RELEASE_EIP; then
  EIP_ALLOCS=$(aws ec2 describe-addresses \
    --filters "Name=tag:Project,Values=${MM_PROJECT_TAG}" \
              "Name=tag:Role,Values=demo" \
    --query 'Addresses[].AllocationId' \
    --output text --region "$REGION" 2>/dev/null || true)

  if [ -n "$EIP_ALLOCS" ]; then
    for alloc in $EIP_ALLOCS; do
      echo "Releasing EIP: $alloc"
      aws ec2 release-address --allocation-id "$alloc" --region "$REGION" 2>/dev/null || true
    done
  fi
fi

# Clean up launch file
rm -f "$LAUNCH_FILE"

echo ""
echo "Demo teardown complete."
