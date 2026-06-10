# Task: Disconnect accounts with email-address names, revoke OAuth with period in name.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Connected accounts whose accountName is an email address:
    #   Figma: "alex.morgan@acmecorp.io" → disconnect
    #   Google: "alex.morgan@gmail.com" → disconnect
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    for name in ("Figma", "Google"):
        if name in providers:
            failures.append(f"'{name}' should have been disconnected (account name is an email)")
    for name in ("GitHub", "GitLab", "Slack"):
        if name not in providers:
            failures.append(f"'{name}' should remain (account name is not an email)")

    # OAuth app whose name contains a period: Marker.io → revoke
    apps = state.get("authorizedApps", [])
    app_names = [a.get("name") for a in apps]
    if "Marker.io" in app_names:
        failures.append("'Marker.io' should have been revoked (name contains a period)")

    if failures:
        return False, "; ".join(failures)
    return True, "Email-address accounts disconnected and Marker.io revoked."
