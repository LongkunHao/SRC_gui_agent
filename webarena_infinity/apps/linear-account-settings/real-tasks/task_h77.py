# Task: Revoke earliest-created API key, register passkey with its label.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Earliest created API key: Monitoring Dashboard (2025-04-02)
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    if "Monitoring Dashboard" in key_labels:
        failures.append("'Monitoring Dashboard' API key should have been revoked (earliest created)")

    # Passkey named "Monitoring Dashboard"
    passkeys = state.get("passkeys", [])
    pk_names = [p.get("name") for p in passkeys]
    if "Monitoring Dashboard" not in pk_names:
        failures.append("Expected a passkey named 'Monitoring Dashboard'")

    if failures:
        return False, "; ".join(failures)
    return True, "Earliest API key revoked and passkey 'Monitoring Dashboard' registered."
