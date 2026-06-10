# Task: Turn on cycle updates for every currently-enabled notification channel.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    # Desktop, mobile, email were enabled at seed; slack was disabled
    for channel in ("desktop", "mobile", "email"):
        ch = ns.get(channel, {})
        if not ch.get("cycleUpdated"):
            failures.append(f"{channel} cycleUpdated should be true (channel was enabled)")

    # Slack was disabled — should remain unchanged (cycleUpdated = false)
    slack = ns.get("slack", {})
    if slack.get("cycleUpdated"):
        failures.append("slack cycleUpdated should remain false (channel was disabled)")

    if failures:
        return False, "; ".join(failures)
    return True, "Cycle updates enabled for all originally-enabled channels; slack unchanged."
