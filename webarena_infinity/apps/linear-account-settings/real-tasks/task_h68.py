# Task: Count passkeys, revoke that many most-recently-authorized OAuth apps.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Seed: 3 passkeys → revoke 3 most recently authorized OAuth apps
    # By authorizedAt: Screenful (2026-01-08), Marker.io (2025-12-15), Linear Exporter (2025-11-01)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]

    for name in ("Screenful", "Marker.io", "Linear Exporter"):
        if name in app_names:
            failures.append(f"'{name}' should have been revoked (among 3 most recently authorized)")

    for name in ("Raycast", "Notion Integration", "Zapier"):
        if name not in app_names:
            failures.append(f"'{name}' should not have been revoked")

    if failures:
        return False, "; ".join(failures)
    return True, "Revoked 3 most recently authorized OAuth apps (matching passkey count)."
