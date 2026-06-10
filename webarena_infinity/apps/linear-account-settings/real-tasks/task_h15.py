# Task: Disconnect Slack and Google connected accounts, then disable Slack notifications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    connected = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in connected]

    failures = []
    if "Slack" in providers:
        failures.append("Slack connected account still present")
    if "Google" in providers:
        failures.append("Google connected account still present")

    slack_notif = state.get("notificationSettings", {}).get("slack", {})
    if slack_notif.get("enabled") != False:
        failures.append(f"Slack notifications enabled: expected False, got {slack_notif.get('enabled')}")

    if failures:
        return False, "; ".join(failures)
    return True, "Slack and Google disconnected, Slack notifications disabled."
