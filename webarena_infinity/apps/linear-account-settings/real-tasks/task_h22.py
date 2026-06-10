# Task: Revoke all sessions from outside California, then create API key 'West Coast Only'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    sessions = state.get("sessions", [])
    non_ca = [s for s in sessions if ", CA," not in s.get("location", "")]
    if non_ca:
        names = [s.get("deviceName") for s in non_ca]
        failures.append(f"Non-California sessions still present: {names}")

    ca_sessions = [s for s in sessions if ", CA," in s.get("location", "")]
    if len(ca_sessions) < 1:
        failures.append("No California sessions remain")

    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]
    if "West Coast Only" not in labels:
        failures.append(f"API key 'West Coast Only' not found. Current keys: {labels}")

    if failures:
        return False, "; ".join(failures)
    return True, "Non-California sessions revoked and 'West Coast Only' API key created."
