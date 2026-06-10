# Task: Revoke API keys created same year as passkeys, remove newest passkey.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # All passkeys created in 2025 → revoke API keys from 2025
    # API keys from 2025: CI/CD Pipeline, Slack Bot, Data Export, Monitoring Dashboard
    # Keep: Mobile App Testing (2026)
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    for label in ("CI/CD Pipeline", "Slack Bot Integration", "Data Export Script", "Monitoring Dashboard"):
        if label in key_labels:
            failures.append(f"API key '{label}' should have been revoked (created in 2025)")
    if "Mobile App Testing" not in key_labels:
        failures.append("'Mobile App Testing' should remain (created in 2026)")

    # Most recently registered passkey: iPhone Face ID (2025-11-10) → remove
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "iPhone Face ID" in pk_names:
        failures.append("'iPhone Face ID' should have been removed (most recently registered)")

    if failures:
        return False, "; ".join(failures)
    return True, "2025 API keys revoked and newest passkey removed."
