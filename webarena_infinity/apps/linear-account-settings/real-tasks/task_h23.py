# Task: Revoke the API key last used the longest ago, and the OAuth app authorized earliest.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Mobile App Testing was last used longest ago (2026-01-20)
    api_keys = state.get("apiKeys", [])
    labels = [k.get("label") for k in api_keys]
    if "Mobile App Testing" in labels:
        failures.append("'Mobile App Testing' API key still present (last used longest ago)")

    # Zapier was authorized earliest (2025-05-20)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Zapier" in app_names:
        failures.append("'Zapier' OAuth app still present (authorized earliest)")

    if failures:
        return False, "; ".join(failures)
    return True, "Least recently used API key and earliest authorized OAuth app revoked."
