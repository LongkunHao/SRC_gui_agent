# Task: Revoke odd-month OAuth apps, disconnect even-month connected accounts.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # OAuth authorized in odd months:
    #   Zapier (May=5), Raycast (Jul=7), Notion (Sep=9),
    #   Linear Exporter (Nov=11), Screenful (Jan=1) → revoke all
    # Keep: Marker.io (Dec=12, even)
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    for name in ("Zapier", "Raycast", "Notion Integration", "Linear Exporter", "Screenful"):
        if name in app_names:
            failures.append(f"'{name}' should have been revoked (authorized in odd month)")
    if "Marker.io" not in app_names:
        failures.append("'Marker.io' should remain (authorized in even month December)")

    # Connected accounts linked in even months:
    #   GitHub (Jun=6), GitLab (Aug=8), Slack (Jun=6), Google (Jun=6) → disconnect
    # Keep: Figma (Jan=1, odd)
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    for name in ("GitHub", "GitLab", "Slack", "Google"):
        if name in providers:
            failures.append(f"'{name}' should have been disconnected (linked in even month)")
    if "Figma" not in providers:
        failures.append("'Figma' should remain (linked in odd month January)")

    if failures:
        return False, "; ".join(failures)
    return True, "Odd-month OAuth apps revoked and even-month accounts disconnected."
