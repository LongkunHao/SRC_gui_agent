# Task: Revoke all API keys created before 2026, create 'Primary' and 'Backup'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]

    # Pre-2026 keys should be gone: CI/CD Pipeline, Slack Bot Integration, Data Export Script, Monitoring Dashboard
    for old_label in ("CI/CD Pipeline", "Slack Bot Integration", "Data Export Script", "Monitoring Dashboard"):
        if old_label in labels:
            failures.append(f"'{old_label}' should have been revoked (created before 2026)")

    # Mobile App Testing (created Jan 2026) should remain
    if "Mobile App Testing" not in labels:
        failures.append("'Mobile App Testing' should still exist (created in 2026)")

    # New keys
    if "Primary" not in labels:
        failures.append("Expected an API key labeled 'Primary'")
    if "Backup" not in labels:
        failures.append("Expected an API key labeled 'Backup'")

    if failures:
        return False, "; ".join(failures)
    return True, "Pre-2026 API keys revoked; 'Primary' and 'Backup' keys created."
