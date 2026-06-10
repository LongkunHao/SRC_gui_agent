# Task: For enabled notification channels, turn off all types but keep channel enabled. Leave disabled channels.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    notif_types = ("issueAssigned", "issueStatusChanged", "issueCommented",
                   "issueMentioned", "projectUpdated", "cycleUpdated")

    # Desktop, Mobile, Email were enabled — types should all be false, channel stays enabled
    for channel in ("desktop", "mobile", "email"):
        ch = ns.get(channel, {})
        if not ch.get("enabled"):
            failures.append(f"{channel} should still be enabled")
        for key in notif_types:
            if ch.get(key):
                failures.append(f"{channel}.{key} should be false")

    # Slack was disabled — should remain unchanged
    slack = ns.get("slack", {})
    if slack.get("enabled"):
        failures.append("Slack should still be disabled (was disabled before)")

    if failures:
        return False, "; ".join(failures)
    return True, "All notification types disabled for enabled channels; disabled channels untouched."
