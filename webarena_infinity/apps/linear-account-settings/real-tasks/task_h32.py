# Task: Revoke all OAuth apps with read:teams permission, leave workspace with fewest members.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    apps = state.get("authorizedApps", [])
    teams_apps = [a for a in apps if "read:teams" in a.get("permissions", [])]
    if teams_apps:
        names = [a.get("name") for a in teams_apps]
        failures.append(f"Apps with read:teams still present: {names}")

    # Raycast is the only app without read:teams — it should remain
    app_names = [a.get("name") for a in apps]
    if "Raycast" not in app_names:
        failures.append("'Raycast' was incorrectly revoked (does not have read:teams)")

    # Side Project Labs has fewest members (8)
    workspaces = state.get("workspaces", [])
    ws_names = [w.get("name") for w in workspaces]
    if "Side Project Labs" in ws_names:
        failures.append("'Side Project Labs' still present (fewest members)")

    if failures:
        return False, "; ".join(failures)
    return True, "OAuth apps with read:teams revoked and smallest workspace left."
