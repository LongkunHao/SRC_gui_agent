# Task: Full lockdown — disable all notification channels, disconnect all accounts, revoke all apps.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    ns = state.get("notificationSettings", {})
    for channel in ("desktop", "mobile", "email", "slack"):
        ch = ns.get(channel, {})
        if ch.get("enabled"):
            failures.append(f"{channel} notifications still enabled")

    accounts = state.get("connectedAccounts", [])
    if accounts:
        names = [a.get("provider") for a in accounts]
        failures.append(f"Connected accounts still present: {names}")

    apps = state.get("authorizedApps", [])
    if apps:
        names = [a.get("name") for a in apps]
        failures.append(f"Authorized apps still present: {names}")

    if failures:
        return False, "; ".join(failures)
    return True, "Full lockdown complete: all channels disabled, accounts disconnected, apps revoked."
