# Task: Create API key named after app with most permissions, then revoke that app.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Zapier has the most permissions (5). Create API key "Zapier", revoke Zapier.
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    if "Zapier" not in key_labels:
        failures.append("Expected an API key labeled 'Zapier'")

    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Zapier" in app_names:
        failures.append("Zapier OAuth app should have been revoked")

    if failures:
        return False, "; ".join(failures)
    return True, "API key 'Zapier' created and Zapier OAuth app revoked."
