# Task: Revoke tablet sessions, disconnect accounts with >2 scopes, disable all comms.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Tablet sessions: Safari on iPad (sess_06, deviceType=tablet)
    sessions = state.get("sessions", [])
    for s in sessions:
        if s.get("deviceType") == "tablet":
            failures.append(f"Tablet session '{s.get('deviceName')}' should have been revoked")

    # Accounts with >2 scopes: GitHub (3: repo, read:org, read:user)
    # Others: GitLab(2), Slack(2), Figma(1), Google(2) → keep
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "GitHub" in providers:
        failures.append("'GitHub' should have been disconnected (3 scopes, >2)")
    for kept in ("GitLab", "Slack", "Figma", "Google"):
        if kept not in providers:
            failures.append(f"'{kept}' should still be connected")

    # All comms disabled
    ns = state.get("notificationSettings", {})
    if ns.get("receiveChangelogs") is not False:
        failures.append("receiveChangelogs should be false")
    if ns.get("receiveDpaUpdates") is not False:
        failures.append("receiveDpaUpdates should be false")
    if ns.get("receiveProductUpdates") is not False:
        failures.append("receiveProductUpdates should be false")

    if failures:
        return False, "; ".join(failures)
    return True, "Tablet sessions revoked, >2-scope accounts disconnected, comms disabled."
