#!/usr/bin/env bash
# Run pipeline in batches: launch N environments at a time, wait for all
# to finish, tear down ONLY that batch's instances, then launch the next batch.
#
# Prerequisites: same as launch.sh (GITHUB_TOKEN, KEY_PAIR_NAME, etc.)
#
# Usage:
#   bash infra/setup/run_batches.sh --manifest infra/env_manifest.jsonl --batch-size 3 --model gemini-flash
#   bash infra/setup/run_batches.sh --manifest infra/env_manifest.jsonl --batch-size 3 --ami ami-0abc123

set -euo pipefail

MANIFEST=""
BATCH_SIZE=3
POLL_INTERVAL=1200  # seconds between completion checks
LAUNCH_ARGS=()

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --manifest)      MANIFEST="$2";      shift 2 ;;
    --batch-size)    BATCH_SIZE="$2";     shift 2 ;;
    --poll-interval) POLL_INTERVAL="$2";  shift 2 ;;
    *)               LAUNCH_ARGS+=("$1"); shift ;;
  esac
done

if [ -z "$MANIFEST" ]; then
  echo "ERROR: --manifest is required"
  echo "Usage: bash infra/setup/run_batches.sh --manifest FILE --batch-size N [launch.sh flags...]"
  exit 1
fi

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: Manifest not found: $MANIFEST"
  exit 1
fi

# --- Read all environments ---
ALL_ENVS=()
while IFS= read -r line; do
  [ -z "$line" ] && continue
  ALL_ENVS+=("$line")
done < "$MANIFEST"
TOTAL=${#ALL_ENVS[@]}

if [ "$TOTAL" -eq 0 ]; then
  echo "ERROR: No environments in $MANIFEST"
  exit 1
fi

NUM_BATCHES=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))
echo "=== Batch Run Plan ==="
echo "  Total environments: $TOTAL"
echo "  Batch size:         $BATCH_SIZE"
echo "  Number of batches:  $NUM_BATCHES"
echo "  Poll interval:      ${POLL_INTERVAL}s"
echo "  Extra launch args:  ${LAUNCH_ARGS[*]:-none}"
echo ""

# --- Load central config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config.sh"

REGION="$MM_REGION"
KEY_PAIR="${KEY_PAIR_NAME:-}"

SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -o BatchMode=yes"

# ============================================================
# check_instance_status INSTANCE_ID
#   Prints a status line and echoes one of: running, done, crashed, unknown
# ============================================================
check_instance_status() {
  local inst_id="$1"

  local info
  info=$(aws ec2 describe-instances --instance-ids "$inst_id" \
    --query 'Reservations[0].Instances[0].[PublicIpAddress,State.Name,Tags[?Key==`EnvId`].Value|[0]]' \
    --output text --region "$REGION" 2>/dev/null) || { echo "unknown"; return; }

  local ip state env_id
  ip=$(echo "$info" | awk '{print $1}')
  state=$(echo "$info" | awk '{print $2}')
  env_id=$(echo "$info" | awk '{print $3}')

  # Instance not running (terminated/stopped)
  if [ "$state" != "running" ]; then
    echo "    $env_id ($inst_id): instance $state" >&2
    echo "done"
    return
  fi

  if [ "$ip" = "None" ] || [ -z "$ip" ]; then
    echo "    $env_id ($inst_id): no public IP yet" >&2
    echo "running"
    return
  fi

  # Check if pipeline process is alive
  local pipeline_alive
  pipeline_alive=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" $SSH_OPTS \
    "ec2-user@${ip}" \
    'pgrep -f "infra/pipeline[.]py" > /dev/null 2>&1 && echo yes || echo no' \
    2>/dev/null) || pipeline_alive="unreachable"

  if [ "$pipeline_alive" = "yes" ]; then
    # Still running — grab latest status line
    local status_line
    status_line=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" $SSH_OPTS \
      "ec2-user@${ip}" \
      'grep -E "(Phase|pass rate|complete|iteration)" /tmp/mirror-mirror-logs/pipeline.log 2>/dev/null | tail -1 | sed "s/^[0-9-]* [0-9:]* \[pipeline\] //"' \
      2>/dev/null) || status_line="unknown"
    echo "    $env_id: RUNNING — $status_line" >&2
    echo "running"
    return
  fi

  if [ "$pipeline_alive" = "unreachable" ]; then
    echo "    $env_id: SSH unreachable" >&2
    echo "running"  # treat as still going — may be transient
    return
  fi

  # Pipeline process is gone — did it finish or crash?
  local completed
  completed=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" $SSH_OPTS \
    "ec2-user@${ip}" \
    'grep -c "Pipeline complete for:" /tmp/mirror-mirror-logs/pipeline.log 2>/dev/null || echo 0' \
    2>/dev/null) || completed="0"

  if [ "$completed" != "0" ]; then
    echo "    $env_id: DONE" >&2
    echo "done"
  else
    local fail_msg
    fail_msg=$(ssh -i "$HOME/.ssh/${KEY_PAIR}.pem" $SSH_OPTS \
      "ec2-user@${ip}" \
      'grep -E "FAILED|Error|Traceback" /tmp/mirror-mirror-logs/pipeline.log 2>/dev/null | tail -1 | sed "s/^[0-9-]* [0-9:]* \[pipeline\] //"' \
      2>/dev/null) || fail_msg="unknown error"
    echo "    $env_id: CRASHED — ${fail_msg:-(no log)}" >&2
    echo "crashed"
  fi
}

# ============================================================
# check_batch_done INSTANCE_ID [INSTANCE_ID ...]
#   Returns 0 if all instances are finished (done or crashed).
#   Sets BATCH_RESULTS associative array with per-instance outcomes.
# ============================================================
declare -A BATCH_RESULTS
check_batch_done() {
  local all_done=true
  BATCH_RESULTS=()

  for inst_id in "$@"; do
    local result
    result=$(check_instance_status "$inst_id")
    BATCH_RESULTS["$inst_id"]="$result"
    if [ "$result" = "running" ] || [ "$result" = "unknown" ]; then
      all_done=false
    fi
  done

  $all_done
}

# ============================================================
# teardown_instances INSTANCE_ID [INSTANCE_ID ...]
#   Stops specific instances and disassociates their EIPs (returns to pool).
#   Does NOT touch any other mirror-mirror instances.
# ============================================================
teardown_instances() {
  local ids=("$@")
  if [ ${#ids[@]} -eq 0 ]; then
    echo "  No instances to tear down."
    return
  fi

  # Disassociate EIPs (return to pool, don't release)
  for inst_id in "${ids[@]}"; do
    local assoc_id
    assoc_id=$(aws ec2 describe-addresses \
      --filters "Name=instance-id,Values=$inst_id" \
      --query 'Addresses[0].AssociationId' --output text --region "$REGION" 2>/dev/null) || continue
    if [ -n "$assoc_id" ] && [ "$assoc_id" != "None" ]; then
      aws ec2 disassociate-address --association-id "$assoc_id" --region "$REGION" 2>/dev/null || true
      echo "  Disassociated EIP from $inst_id"
    fi
  done

  # Stop instances (not terminate — preserves EBS for debugging if needed)
  local running_ids=()
  for inst_id in "${ids[@]}"; do
    local state
    state=$(aws ec2 describe-instances --instance-ids "$inst_id" \
      --query 'Reservations[0].Instances[0].State.Name' --output text --region "$REGION" 2>/dev/null) || continue
    if [ "$state" = "running" ] || [ "$state" = "pending" ]; then
      running_ids+=("$inst_id")
    fi
  done

  if [ ${#running_ids[@]} -gt 0 ]; then
    echo "  Stopping ${#running_ids[@]} instance(s): ${running_ids[*]}"
    aws ec2 stop-instances --instance-ids "${running_ids[@]}" --region "$REGION" > /dev/null
    echo "  Waiting for instances to stop..."
    aws ec2 wait instance-stopped --instance-ids "${running_ids[@]}" --region "$REGION"
    echo "  Stopped."
  else
    echo "  All instances already stopped."
  fi
}

# --- Run batches ---
FAILED_BATCHES=()

for (( batch=0; batch<NUM_BATCHES; batch++ )); do
  start=$(( batch * BATCH_SIZE ))
  end=$(( start + BATCH_SIZE ))
  if [ "$end" -gt "$TOTAL" ]; then
    end=$TOTAL
  fi
  batch_num=$(( batch + 1 ))
  batch_count=$(( end - start ))

  echo "==========================================="
  echo "=== Batch $batch_num / $NUM_BATCHES ($batch_count environments) ==="
  echo "==========================================="
  echo ""

  # Write temp manifest for this batch
  BATCH_MANIFEST=$(mktemp /tmp/mm-batch-XXXXXX.jsonl)
  for (( i=start; i<end; i++ )); do
    echo "${ALL_ENVS[$i]}" >> "$BATCH_MANIFEST"
  done

  echo "Environments in this batch:"
  while IFS= read -r line; do
    env_id=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['env_id'])")
    echo "  - $env_id"
  done < "$BATCH_MANIFEST"
  echo ""

  # Launch this batch
  LAUNCH_FILE="/tmp/mirror-mirror-launch-batch${batch_num}.env"
  if ! bash infra/setup/launch.sh --manifest "$BATCH_MANIFEST" --launch-file "$LAUNCH_FILE" "${LAUNCH_ARGS[@]}"; then
    echo ""
    echo "ERROR: launch.sh failed for batch $batch_num"
    rm -f "$BATCH_MANIFEST"
    FAILED_BATCHES+=("$batch_num")
    continue
  fi

  # Read instance IDs from the launch file
  BATCH_INSTANCE_IDS=""
  BATCH_KEY_PAIR=""
  # Use a subshell to avoid launch file vars leaking into our scope
  eval "$(grep '^INSTANCE_IDS=' "$LAUNCH_FILE")"
  BATCH_INSTANCE_IDS="$INSTANCE_IDS"
  # Restore our KEY_PAIR (launch file may have overwritten it)
  if [ -z "$KEY_PAIR" ]; then
    eval "$(grep '^KEY_PAIR=' "$LAUNCH_FILE")"
  fi

  # Convert to array
  read -ra BATCH_IDS <<< "$BATCH_INSTANCE_IDS"

  if [ ${#BATCH_IDS[@]} -eq 0 ]; then
    echo "ERROR: No instance IDs found in $LAUNCH_FILE"
    rm -f "$BATCH_MANIFEST"
    FAILED_BATCHES+=("$batch_num")
    continue
  fi

  echo ""
  echo "=== Waiting for batch $batch_num to complete (polling every ${POLL_INTERVAL}s) ==="
  echo "  Tracking ${#BATCH_IDS[@]} instance(s): ${BATCH_IDS[*]}"
  echo ""

  while true; do
    echo "--- Poll $(date -u +%H:%M:%S) ---"
    if check_batch_done "${BATCH_IDS[@]}"; then
      echo ""
      break
    fi
    echo "  --- sleeping ${POLL_INTERVAL}s ---"
    echo ""
    sleep "$POLL_INTERVAL"
  done

  # Summarize results
  had_failures=false
  had_crashes=false
  done_ids=()
  crashed_ids=()

  for inst_id in "${BATCH_IDS[@]}"; do
    case "${BATCH_RESULTS[$inst_id]:-unknown}" in
      done)    done_ids+=("$inst_id") ;;
      crashed) crashed_ids+=("$inst_id"); had_crashes=true; had_failures=true ;;
      *)       crashed_ids+=("$inst_id"); had_failures=true ;;
    esac
  done

  echo "=== Batch $batch_num Summary ==="
  echo "  Succeeded: ${#done_ids[@]}"
  echo "  Failed:    ${#crashed_ids[@]}"

  if $had_crashes; then
    echo ""
    echo "  Failed instances kept alive for debugging:"
    for inst_id in "${crashed_ids[@]}"; do
      local_ip=$(aws ec2 describe-instances --instance-ids "$inst_id" \
        --query 'Reservations[0].Instances[0].PublicIpAddress' --output text --region "$REGION" 2>/dev/null)
      local_env=$(aws ec2 describe-instances --instance-ids "$inst_id" \
        --query 'Reservations[0].Instances[0].Tags[?Key==`EnvId`].Value|[0]' --output text --region "$REGION" 2>/dev/null)
      echo "    $local_env: ssh -i ~/.ssh/${KEY_PAIR}.pem ec2-user@${local_ip}"
    done
    FAILED_BATCHES+=("$batch_num")
  fi

  # Tear down successful instances (batch-scoped, not global)
  if [ ${#done_ids[@]} -gt 0 ]; then
    echo ""
    echo "=== Tearing down ${#done_ids[@]} succeeded instance(s) from batch $batch_num ==="
    teardown_instances "${done_ids[@]}"
  fi

  # Clean up temp files
  rm -f "$BATCH_MANIFEST"
  rm -f "$LAUNCH_FILE"

  echo ""
  if [ "$batch_num" -lt "$NUM_BATCHES" ]; then
    echo "Moving to next batch..."
    echo ""
  fi
done

echo "==========================================="
echo "=== All $NUM_BATCHES batches processed ==="
echo "==========================================="

if [ ${#FAILED_BATCHES[@]} -gt 0 ]; then
  echo ""
  echo "WARNING: Batches with failures: ${FAILED_BATCHES[*]}"
  echo "  Failed instances are still running. Investigate, then tear down manually:"
  echo "    bash infra/setup/teardown.sh"
  exit 1
else
  echo "All batches completed successfully!"
fi
