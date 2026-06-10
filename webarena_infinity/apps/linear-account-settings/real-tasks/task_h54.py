# Task: Revoke API keys without expiry, create 'Replacement', enable both auto-assigns.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]

    # No-expiry keys should be revoked: CI/CD Pipeline, Data Export Script, Monitoring Dashboard
    for revoked in ("CI/CD Pipeline", "Data Export Script", "Monitoring Dashboard"):
        if revoked in labels:
            failures.append(f"'{revoked}' should have been revoked (no expiration)")

    # Keys with expiry should remain: Slack Bot Integration, Mobile App Testing
    for kept in ("Slack Bot Integration", "Mobile App Testing"):
        if kept not in labels:
            failures.append(f"'{kept}' should still exist (has expiration)")

    # New key 'Replacement'
    if "Replacement" not in labels:
        failures.append("Expected an API key labeled 'Replacement'")

    # Both auto-assign settings enabled
    prefs = state.get("preferences", {})
    if prefs.get("autoAssignOnCreate") is not True:
        failures.append("autoAssignOnCreate should be true")
    if prefs.get("autoAssignOnStarted") is not True:
        failures.append("autoAssignOnStarted should be true")

    if failures:
        return False, "; ".join(failures)
    return True, "No-expiry keys revoked, 'Replacement' created, both auto-assigns enabled."
