#!/usr/bin/env bash
# Poll instances for setup completion, then start pipelines via SSH.
#
# Reads instance info from /tmp/mirror-mirror-launch.env and pipeline
# config from the manifest. Safe to re-run — skips instances that
# already have a running pipeline.
#
# Usage:
#   bash infra/setup/start_pipelines.sh --manifest infra/env_manifest.jsonl
#   bash infra/setup/start_pipelines.sh --manifest infra/env_manifest.jsonl --launch-file /tmp/mm.env

set -uo pipefail

LAUNCH_FILE="/tmp/mirror-mirror-launch.env"
MANIFEST=""
MAX_WAIT=300      # 5 minutes
POLL_INTERVAL=15  # seconds

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --manifest)      MANIFEST="$2";      shift 2 ;;
    --launch-file)   LAUNCH_FILE="$2";   shift 2 ;;
    --max-wait)      MAX_WAIT="$2";      shift 2 ;;
    --poll-interval) POLL_INTERVAL="$2"; shift 2 ;;
    *)
      echo "Usage: bash infra/setup/start_pipelines.sh --manifest FILE [--launch-file FILE]"
      exit 1
      ;;
  esac
done

if [ -z "$MANIFEST" ]; then
  echo "ERROR: --manifest is required"
  exit 1
fi

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: Manifest not found: $MANIFEST"
  exit 1
fi

if [ ! -f "$LAUNCH_FILE" ]; then
  echo "ERROR: Launch file not found: $LAUNCH_FILE"
  echo "Run launch.sh first."
  exit 1
fi

source "$LAUNCH_FILE"
KEY_PAIR="${KEY_PAIR:-${KEY_PAIR_NAME:-}}"
REGION="${REGION:-${AWS_REGION:-us-east-1}}"
SSH_OPTS="-i $HOME/.ssh/${KEY_PAIR}.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5"

# --- Read manifest into lookup ---
ENVS=()
while IFS= read -r line; do
  [ -z "$line" ] && continue
  ENVS+=("$line")
done < "$MANIFEST"

# Helper: look up docs_path for an env_id
lookup_docs() {
  local target="$1"
  for entry in "${ENVS[@]}"; do
    eid=$(echo "$entry" | python3 -c "import sys,json; print(json.load(sys.stdin)['env_id'])")
    if [ "$eid" = "$target" ]; then
      echo "$entry" | python3 -c "import sys,json; print(json.load(sys.stdin)['docs_path'])"
      return
    fi
  done
  echo ""
}

# --- Gather instance info ---
ALL_IPS=""
ALL_ENVS=""
ALL_DOCS=""

for INST_ID in $INSTANCE_IDS; do
  INFO=$(aws ec2 describe-instances --instance-ids "$INST_ID" \
    --query 'Reservations[0].Instances[0].[PublicIpAddress,Tags[?Key==`EnvId`].Value|[0]]' \
    --output text --region "$REGION" 2>/dev/null)
  IP=$(echo "$INFO" | awk '{print $1}')
  ENV_ID=$(echo "$INFO" | awk '{print $2}')
  DOCS=$(lookup_docs "$ENV_ID")

  ALL_IPS="$ALL_IPS $IP"
  ALL_ENVS="$ALL_ENVS $ENV_ID"
  ALL_DOCS="$ALL_DOCS $DOCS"
done

IPS=($ALL_IPS)
ENV_IDS=($ALL_ENVS)
DOCS_PATHS=($ALL_DOCS)

# --- Wait for setup to complete ---
echo "=== Waiting for setup to complete on ${#IPS[@]} instances ==="

for i in "${!IPS[@]}"; do
  IP="${IPS[$i]}"
  ENV_ID="${ENV_IDS[$i]}"
  elapsed=0

  printf "  %-30s " "$ENV_ID"

  # Skip if pipeline already running
  ALREADY=$(ssh $SSH_OPTS "ec2-user@${IP}" 'pgrep -f "infra/pipeline[.]py" > /dev/null 2>&1 && echo yes || echo no' 2>/dev/null || echo "no")
  if [ "$ALREADY" = "yes" ]; then
    echo "already running"
    continue
  fi

  printf "waiting..."
  while [ $elapsed -lt $MAX_WAIT ]; do
    READY=$(ssh $SSH_OPTS "ec2-user@${IP}" "test -f ~/.setup-complete && test -d ~/mirror-mirror/.git && echo yes || echo no" 2>/dev/null || echo "unreachable")
    if [ "$READY" = "yes" ]; then
      echo " ready"
      break
    fi
    sleep $POLL_INTERVAL
    elapsed=$((elapsed + POLL_INTERVAL))
  done

  if [ $elapsed -ge $MAX_WAIT ]; then
    echo " TIMEOUT"
  fi
done

# --- Start pipelines ---
echo ""
echo "=== Starting pipelines ==="

for i in "${!IPS[@]}"; do
  IP="${IPS[$i]}"
  ENV_ID="${ENV_IDS[$i]}"
  DOCS="${DOCS_PATHS[$i]}"

  # Skip if already running
  ALREADY=$(ssh $SSH_OPTS "ec2-user@${IP}" 'pgrep -f "infra/pipeline[.]py" > /dev/null 2>&1 && echo yes || echo no' 2>/dev/null || echo "no")
  if [ "$ALREADY" = "yes" ]; then
    echo "  SKIP $ENV_ID — already running"
    continue
  fi

  # Verify clone exists
  CLONE_OK=$(ssh $SSH_OPTS "ec2-user@${IP}" "test -d ~/mirror-mirror/.git && echo yes || echo no" 2>/dev/null || echo "no")
  if [ "$CLONE_OK" != "yes" ]; then
    echo "  SKIP $ENV_ID — setup incomplete (ssh -i ~/.ssh/${KEY_PAIR}.pem ec2-user@${IP})"
    continue
  fi

  # Run smoke test on the instance before starting pipeline
  echo "  Smoke testing $ENV_ID @ $IP ..."
  SMOKE_OUTPUT=$(ssh $SSH_OPTS "ec2-user@${IP}" \
    "source ~/.bashrc && cd ~/mirror-mirror && bash infra/smoke_test.sh --model ${MODEL}" 2>&1)
  SMOKE_RC=$?
  if [ "$SMOKE_RC" -ne 0 ]; then
    echo "  FAIL $ENV_ID — smoke test failed (ssh -i ~/.ssh/${KEY_PAIR}.pem ec2-user@${IP})"
    echo "$SMOKE_OUTPUT" | sed 's/^/       /'
    continue
  fi
  echo "  OK   $ENV_ID — smoke test passed"

  PIPELINE_CMD="cd ~/mirror-mirror && \$HOME/venv/bin/python infra/pipeline.py \
    --app-name ${ENV_ID} \
    --docs-path ${DOCS} \
    --model ${MODEL} \
    --workers ${WORKERS} \
    --repetitions ${REPETITIONS} \
    --max-iterations ${MAX_ITERATIONS} \
    --branch ${ENV_ID} \
    --s3-bucket \$MM_S3_BUCKET \
    > /tmp/mirror-mirror-logs/pipeline.log 2>&1"

  ssh -n $SSH_OPTS "ec2-user@${IP}" "screen -dm bash -c '$PIPELINE_CMD'" </dev/null
  echo "  STARTED $ENV_ID @ $IP"
done

echo ""
echo "Monitor progress:"
echo "  bash infra/setup/monitor.sh"
