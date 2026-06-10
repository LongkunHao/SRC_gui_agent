# Task: Revoke read-only OAuth apps, create API key per revoked app.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Read-only apps (no write perms): Notion Integration, Linear Exporter, Screenful
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    for name in ("Notion Integration", "Linear Exporter", "Screenful"):
        if name in app_names:
            failures.append(f"'{name}' should have been revoked (read-only)")

    # Apps with write perms should remain
    for name in ("Raycast", "Zapier", "Marker.io"):
        if name not in app_names:
            failures.append(f"'{name}' should not have been revoked (has write permissions)")

    # New API keys created for each revoked app
    api_keys = state.get("apiKeys", [])
    key_labels = [k.get("label") for k in api_keys]
    for name in ("Notion Integration", "Linear Exporter", "Screenful"):
        if name not in key_labels:
            failures.append(f"Expected an API key labeled '{name}'")

    if failures:
        return False, "; ".join(failures)
    return True, "Revoked read-only OAuth apps and created corresponding API keys."
