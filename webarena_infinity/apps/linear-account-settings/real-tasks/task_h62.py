# Task: Revoke OAuth apps whose permission count equals count of same-domain connected accounts.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Seed: 4 connected accounts share acmecorp.io domain
    # OAuth apps with exactly 4 permissions: Linear Exporter (4), Screenful (4)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]

    for name in ("Linear Exporter", "Screenful"):
        if name in app_names:
            failures.append(f"'{name}' should have been revoked (has 4 permissions = 4 same-domain accounts)")

    # Apps that should remain
    for name in ("Raycast", "Notion Integration", "Zapier", "Marker.io"):
        if name not in app_names:
            failures.append(f"'{name}' should not have been revoked")

    if failures:
        return False, "; ".join(failures)
    return True, "Revoked OAuth apps with permission count matching same-domain account count."
