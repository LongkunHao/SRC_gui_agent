# Task: Conditional channel toggle — enabled→disable+types on, disabled→enable+types off.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []
    types = ("issueAssigned", "issueStatusChanged", "issueCommented",
             "issueMentioned", "projectUpdated", "cycleUpdated")

    # Seed enabled: desktop, mobile, email → now disabled with all types on
    for channel in ("desktop", "mobile", "email"):
        ch = ns.get(channel, {})
        if ch.get("enabled") is not False:
            failures.append(f"{channel} should be disabled")
        for t in types:
            if ch.get(t) is not True:
                failures.append(f"{channel}.{t} should be True")

    # Seed disabled: slack → now enabled with all types off
    slack = ns.get("slack", {})
    if slack.get("enabled") is not True:
        failures.append("slack should be enabled")
    for t in types:
        if slack.get(t) is not False:
            failures.append(f"slack.{t} should be False")

    if failures:
        return False, "; ".join(failures)
    return True, "Channels toggled with conditional type settings applied."
