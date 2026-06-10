# Task: Disconnect write-scope accounts, revoke most-recent OAuth, Light-Contrast theme.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Connected accounts with any write scope: Slack (chat:write) → disconnect
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "Slack" in providers:
        failures.append("Slack should have been disconnected (has write-level scope)")
    for name in ("GitHub", "GitLab", "Figma", "Google"):
        if name not in providers:
            failures.append(f"'{name}' should remain (no write scope)")

    # Most recently accessed OAuth: Raycast (2026-03-06T08:30) → revoke
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Raycast" in app_names:
        failures.append("Raycast should have been revoked (most recently accessed)")

    # Theme: Light - Contrast
    theme = state.get("preferences", {}).get("interfaceTheme", "")
    if theme != "Light - Contrast":
        failures.append(f"Expected theme 'Light - Contrast', got '{theme}'")

    if failures:
        return False, "; ".join(failures)
    return True, "Write-scope account disconnected, Raycast revoked, theme set."
