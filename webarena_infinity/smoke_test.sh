#!/usr/bin/env bash
# Smoke test: verify all external dependencies before running a pipeline.
#
# Usage:
#   bash infra/smoke_test.sh --model gemini
#   bash infra/smoke_test.sh --model gpt

set -uo pipefail

# --- Load central config ---
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$REPO_ROOT/infra/config.sh"

MODEL="gemini"
S3_BUCKET="$MM_S3_BUCKET"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)     MODEL="$2";     shift 2 ;;
    --s3-bucket) S3_BUCKET="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

PASS=0; FAIL=0; SKIP=0
pass() { echo "PASS $1"; PASS=$((PASS + 1)); }
fail() { echo "FAIL $1"; FAIL=$((FAIL + 1)); }
skip() { echo "SKIP $1"; SKIP=$((SKIP + 1)); }

# ── 1. Model API ──
case "$MODEL" in
  gemini|gemini-flash|gemini-pro|gemini-cu)
    if [ -z "${GOOGLE_API_KEY:-}" ]; then fail "GOOGLE_API_KEY not set"; else
      case "$MODEL" in
        gemini-pro) GEMINI_SMOKE_MODEL="gemini-3-pro-preview" ;;
        *)          GEMINI_SMOKE_MODEL="gemini-3-flash-preview" ;;
      esac
      RESP=$(curl -s -w "\n%{http_code}" \
        "https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_SMOKE_MODEL}:generateContent?key=${GOOGLE_API_KEY}" \
        -H 'Content-Type: application/json' \
        -d '{"contents":[{"parts":[{"text":"Say hello in one word"}]}]}' 2>&1)
      HTTP_CODE=$(echo "$RESP" | tail -1); BODY=$(echo "$RESP" | sed '$d')
      if [ "$HTTP_CODE" = "200" ]; then
        SNIPPET=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['candidates'][0]['content']['parts'][0]['text'][:80])" 2>/dev/null || echo "(parse error)")
        pass "Gemini API: $SNIPPET"
      else fail "Gemini API HTTP $HTTP_CODE"; fi
    fi ;;
  gpt)
    if [ -z "${OPENAI_API_KEY:-}" ]; then fail "OPENAI_API_KEY not set"; else
      RESP=$(curl -s -w "\n%{http_code}" "https://api.openai.com/v1/chat/completions" \
        -H "Authorization: Bearer ${OPENAI_API_KEY}" -H 'Content-Type: application/json' \
        -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Say hello in one word"}],"max_tokens":10}' 2>&1)
      HTTP_CODE=$(echo "$RESP" | tail -1); BODY=$(echo "$RESP" | sed '$d')
      if [ "$HTTP_CODE" = "200" ]; then
        SNIPPET=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['choices'][0]['message']['content'][:80])" 2>/dev/null || echo "(parse error)")
        pass "OpenAI API: $SNIPPET"
      else fail "OpenAI API HTTP $HTTP_CODE"; fi
    fi ;;
  claude)
    if [ -z "${ANTHROPIC_API_KEY:-}" ]; then fail "ANTHROPIC_API_KEY not set"; else
      RESP=$(curl -s -w "\n%{http_code}" "https://api.anthropic.com/v1/messages" \
        -H "x-api-key: ${ANTHROPIC_API_KEY}" -H "anthropic-version: 2023-06-01" -H 'Content-Type: application/json' \
        -d '{"model":"claude-haiku-4-5-20251001","max_tokens":10,"messages":[{"role":"user","content":"Say hello in one word"}]}' 2>&1)
      HTTP_CODE=$(echo "$RESP" | tail -1); BODY=$(echo "$RESP" | sed '$d')
      if [ "$HTTP_CODE" = "200" ]; then
        SNIPPET=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['content'][0]['text'][:80])" 2>/dev/null || echo "(parse error)")
        pass "Anthropic API: $SNIPPET"
      else fail "Anthropic API HTTP $HTTP_CODE"; fi
    fi ;;
  *) fail "Unknown model: $MODEL" ;;
esac

# ── 2. Claude CLI ──
if ! command -v claude &>/dev/null; then fail "claude CLI not found"; else
  AUTH=$(claude auth status 2>&1 || true)
  if echo "$AUTH" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('loggedIn') else 1)" 2>/dev/null; then
    AUTH_EMAIL=$(echo "$AUTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email','?'))" 2>/dev/null || echo "?")
    pass "Claude CLI auth ($AUTH_EMAIL)"
  else
    fail "Claude CLI not authenticated"
  fi
  CLAUDE_TMP=$(mktemp /tmp/smoke-claude-XXXXXX)
  # Use script to provide a pseudo-TTY — Claude CLI hangs without one
  script -qc "cd ~/mirror-mirror && timeout 60 claude --dangerously-skip-permissions -p 'Say hello' --max-turns 1 --output-format text" /dev/null > "$CLAUDE_TMP" 2>&1 || true
  HELLO_SHORT=$(tr '\n' ' ' < "$CLAUDE_TMP" | head -c 120)
  if [ -s "$CLAUDE_TMP" ] && ! grep -qi "error\|unauthorized\|denied\|refused\|timed out" "$CLAUDE_TMP"; then
    pass "Claude CLI --dangerously-skip-permissions: $HELLO_SHORT"
  else
    fail "Claude CLI --dangerously-skip-permissions: $HELLO_SHORT"
  fi
  rm -f "$CLAUDE_TMP"
fi

# ── 3a. GitHub Token ──
if [ -z "${GITHUB_TOKEN:-}" ]; then fail "GITHUB_TOKEN not set"; else
  GH_RESP=$(curl -s -w "\n%{http_code}" -H "Authorization: token ${GITHUB_TOKEN}" "https://api.github.com/user" 2>&1)
  GH_HTTP=$(echo "$GH_RESP" | tail -1); GH_BODY=$(echo "$GH_RESP" | sed '$d')
  if [ "$GH_HTTP" = "200" ]; then
    GH_USER=$(echo "$GH_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('login','?'))" 2>/dev/null || echo "?")
    pass "GitHub API ($GH_USER)"
  else fail "GitHub API HTTP $GH_HTTP"; fi
  REMOTE_URL=$(git remote get-url origin 2>/dev/null)
  REPO_SLUG=$(echo "$REMOTE_URL" | sed -E 's#(git@github\.com:|https://([^@]+@)?github\.com/)##; s/\.git$//')
  if [ -n "$REPO_SLUG" ]; then
    DEFAULT_SHA=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
      "https://api.github.com/repos/${REPO_SLUG}/git/refs/heads/main" 2>/dev/null \
      | python3 -c "import sys,json; print(json.load(sys.stdin)['object']['sha'])" 2>/dev/null || echo "")
    if [ -n "$DEFAULT_SHA" ]; then
      TEST_BRANCH="refs/heads/_smoke-test-delete-me-$$"
      CREATE_HTTP=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" -H "Content-Type: application/json" \
        -d "{\"ref\":\"${TEST_BRANCH}\",\"sha\":\"${DEFAULT_SHA}\"}" \
        "https://api.github.com/repos/${REPO_SLUG}/git/refs" 2>/dev/null)
      if [ "$CREATE_HTTP" = "201" ]; then
        curl -s -o /dev/null -X DELETE -H "Authorization: token ${GITHUB_TOKEN}" \
          "https://api.github.com/repos/${REPO_SLUG}/git/${TEST_BRANCH}" 2>/dev/null
        pass "GitHub push access verified"
      else fail "GitHub push denied (HTTP $CREATE_HTTP)"; fi
    else fail "Could not resolve main branch SHA"; fi
  else skip "Could not parse repo slug"; fi
fi

# ── 3b. AWS / S3 ──
if ! command -v aws &>/dev/null; then fail "aws CLI not found"; else
  CALLER=$(aws sts get-caller-identity --query 'Arn' --output text 2>&1)
  if [ $? -eq 0 ]; then pass "AWS credentials ($CALLER)"; else fail "AWS credentials invalid"; fi
  TEST_KEY="_smoke-test-$$.txt"
  if echo "smoke-test" | aws s3 cp - "s3://${S3_BUCKET}/${TEST_KEY}" 2>/dev/null; then
    CONTENT=$(aws s3 cp "s3://${S3_BUCKET}/${TEST_KEY}" - 2>/dev/null)
    aws s3 rm "s3://${S3_BUCKET}/${TEST_KEY}" 2>/dev/null
    if [ "$CONTENT" = "smoke-test" ]; then pass "S3 read+write ($S3_BUCKET)"
    else fail "S3 read-back mismatch"; fi
  else fail "S3 write failed ($S3_BUCKET)"; fi
fi

# ── Summary ──
echo "--- PASS:$PASS FAIL:$FAIL SKIP:$SKIP ---"
if [ "$FAIL" -gt 0 ]; then exit 1; else exit 0; fi
