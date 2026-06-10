# Task: Revoke all OAuth apps that have write permissions.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    apps = state.get("authorizedApps", [])

    write_apps = [a for a in apps if any("write" in p for p in a.get("permissions", []))]
    if write_apps:
        names = [a.get("name", "unknown") for a in write_apps]
        return False, f"Found {len(write_apps)} app(s) with write permissions still present: {names}"

    expected_remaining = {"Notion Integration", "Linear Exporter", "Screenful"}
    actual_remaining = {a.get("name") for a in apps}
    if not expected_remaining.issubset(actual_remaining):
        missing = expected_remaining - actual_remaining
        return False, f"Read-only apps missing: {missing}"

    return True, "All apps with write permissions revoked; read-only apps remain."
