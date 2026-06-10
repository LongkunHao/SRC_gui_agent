# Task: Create API key "Admin-6", revoke OAuth apps with read+write issues.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Role at Acme Corp = Admin, total OAuth apps = 6 → label "Admin-6"
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    if "Admin-6" not in key_labels:
        failures.append("Expected an API key labeled 'Admin-6'")

    # OAuth with read:issues AND write:issues: Raycast, Zapier, Marker.io → revoke
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    for name in ("Raycast", "Zapier", "Marker.io"):
        if name in app_names:
            failures.append(f"'{name}' should have been revoked (has read+write issues)")
    for name in ("Notion Integration", "Linear Exporter", "Screenful"):
        if name not in app_names:
            failures.append(f"'{name}' should remain (read-only on issues)")

    if failures:
        return False, "; ".join(failures)
    return True, "API key 'Admin-6' created and read+write OAuth apps revoked."
