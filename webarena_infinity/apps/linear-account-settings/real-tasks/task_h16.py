# Task: Revoke all API keys that have an expiration date.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    api_keys = state.get("apiKeys", [])

    expiring_keys = [k for k in api_keys if k.get("expiresAt") is not None]
    if expiring_keys:
        labels = [k.get("label", "unknown") for k in expiring_keys]
        return False, f"Found {len(expiring_keys)} API key(s) with expiration still present: {labels}"

    non_expiring = [k.get("label") for k in api_keys]
    expected_remaining = {"CI/CD Pipeline", "Data Export Script", "Monitoring Dashboard"}
    actual_remaining = set(non_expiring)
    if not expected_remaining.issubset(actual_remaining):
        missing = expected_remaining - actual_remaining
        return False, f"Non-expiring keys missing: {missing}"

    return True, "All expiring API keys revoked; non-expiring keys remain."
