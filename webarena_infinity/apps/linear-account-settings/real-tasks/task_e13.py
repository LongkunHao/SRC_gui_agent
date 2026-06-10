# Task: Enable Slack notifications.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("notificationSettings", {}).get("slack", {}).get("enabled")
    if val is True:
        return True, "Slack notifications are enabled"
    return False, f"notificationSettings.slack.enabled is {val}, expected True"
