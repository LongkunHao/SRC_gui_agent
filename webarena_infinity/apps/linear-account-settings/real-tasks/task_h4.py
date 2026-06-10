# Task: Disable all notification channels (desktop, mobile, email, and Slack).
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    notif = state.get("notificationSettings", {})

    for channel in ["desktop", "mobile", "email", "slack"]:
        enabled = notif.get(channel, {}).get("enabled")
        if enabled is not False:
            return False, f"{channel} notifications still enabled (enabled={enabled})"
    return True, "All notification channels disabled."
