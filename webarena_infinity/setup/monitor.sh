#!/usr/bin/env bash
# Simple status checker for self-contained pipeline instances.
#
# SSHs into each running pipeline instance, reads pipeline.log,
# and reports current phase/iteration/pass-rate.
#
# Usage:
#   bash infra/setup/monitor.sh              # single snapshot
#   bash infra/setup/monitor.sh --watch      # continuous (every 60s)
#   bash infra/setup/monitor.sh --watch 30   # continuous (every 30s)

set -uo pipefail

LAUNCH_FILES=()
WATCH=false
INTERVAL=60

while [[ $# -gt 0 ]]; do
  case "$1" in
    --watch)
      WATCH=true
      if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
        INTERVAL="$2"
        shift
      fi
      shift
      ;;
    --launch-file)
      LAUNCH_FILES+=("$2")
      shift 2
      ;;
    *)
      echo "Usage: bash infra/setup/monitor.sh [--watch [SECONDS]] [--launch-file FILE ...]"
      exit 1
      ;;
  esac
done

# Auto-discover launch files if none specified
if [ ${#LAUNCH_FILES[@]} -eq 0 ]; then
  for f in /tmp/mirror-mirror-launch*.env; do
    [ -f "$f" ] && LAUNCH_FILES+=("$f")
  done
fi

if [ ${#LAUNCH_FILES[@]} -eq 0 ]; then
  echo "ERROR: No launch files found. Run launch.sh first."
  exit 1
fi

# Merge INSTANCE_IDS from all launch files
ALL_INSTANCE_IDS=""
for lf in "${LAUNCH_FILES[@]}"; do
  source "$lf"
  ALL_INSTANCE_IDS="$ALL_INSTANCE_IDS $INSTANCE_IDS"
done
INSTANCE_IDS="$ALL_INSTANCE_IDS"
KEY_PAIR="${KEY_PAIR:-${KEY_PAIR_NAME:-}}"
# Load central config for region default
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_SCRIPT_DIR/../config.sh"
REGION="${REGION:-$MM_REGION}"

if [ -z "$KEY_PAIR" ]; then
  echo "ERROR: KEY_PAIR not set (check launch files or set KEY_PAIR_NAME)"
  exit 1
fi

check_status() {
  echo "=== Pipeline Status — $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo ""
  printf "  %-30s %-16s %-12s %s\n" "ENVIRONMENT" "INSTANCE" "STATE" "STATUS"
  printf "  %-30s %-16s %-12s %s\n" "───────────" "────────" "─────" "──────"

  for INST_ID in $INSTANCE_IDS; do
    # Get instance info
    INFO=$(aws ec2 describe-instances --instance-ids "$INST_ID" \
      --query 'Reservations[0].Instances[0].[PublicIpAddress,State.Name,Tags[?Key==`EnvId`].Value|[0]]' \
      --output text --region "$REGION" 2>/dev/null)
    IP=$(echo "$INFO" | awk '{print $1}')
    STATE=$(echo "$INFO" | awk '{print $2}')
    ENV_ID=$(echo "$INFO" | awk '{print $3}')

    if [ "$STATE" != "running" ]; then
      printf "  %-30s %-16s %-12s %s\n" "$ENV_ID" "$INST_ID" "$STATE" "-"
      continue
    fi

    if [ "$IP" = "None" ] || [ -z "$IP" ]; then
      printf "  %-30s %-16s %-12s %s\n" "$ENV_ID" "$INST_ID" "$STATE" "no public IP"
      continue
    fi

    # Check if setup is complete
    SETUP_DONE=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" \
      -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 -o BatchMode=yes \
      "ec2-user@${IP}" "test -f ~/.setup-complete && echo yes || echo no" 2>/dev/null || echo "unreachable")

    if [ "$SETUP_DONE" = "unreachable" ]; then
      printf "  %-30s %-16s %-12s %s\n" "$ENV_ID" "$INST_ID" "$STATE" "SSH unreachable"
      continue
    fi

    if [ "$SETUP_DONE" = "no" ]; then
      printf "  %-30s %-16s %-12s %s\n" "$ENV_ID" "$INST_ID" "$STATE" "setting up..."
      continue
    fi

    # Read pipeline status from log
    STATUS=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" \
      -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 -o BatchMode=yes \
      "ec2-user@${IP}" '
      LOG="/tmp/mirror-mirror-logs/pipeline.log"
      if [ ! -f "$LOG" ]; then
        echo "pipeline not started"
        exit 0
      fi

      # Check if pipeline is running
      if pgrep -f "infra/pipeline[.]py" > /dev/null 2>&1; then
        RUNNING="RUNNING"
      else
        RUNNING="STOPPED"
      fi

      # Get last meaningful log line
      LAST=$(grep -E "(Phase|pass rate|complete|FAILED|iteration)" "$LOG" | tail -1 | sed "s/^[0-9-]* [0-9:]* \[pipeline\] //" 2>/dev/null || echo "unknown")

      echo "${RUNNING}: ${LAST}"
    ' 2>/dev/null || echo "error reading log")

    printf "  %-30s %-16s %-12s %s\n" "$ENV_ID" "${INST_ID:0:12}.." "$STATE" "$STATUS"
  done

  echo ""
}

if [ "$WATCH" = true ]; then
  while true; do
    clear
    check_status
    echo "  Refreshing every ${INTERVAL}s (Ctrl+C to stop)"
    sleep "$INTERVAL"
  done
else
  check_status
fi
