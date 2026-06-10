# Task: All channels enabled; desktop+email types off; mobile+slack types on.
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

    # All channels enabled
    for channel in ("desktop", "mobile", "email", "slack"):
        if ns.get(channel, {}).get("enabled") is not True:
            failures.append(f"{channel} should be enabled")

    # Desktop and email: all types off
    for channel in ("desktop", "email"):
        ch = ns.get(channel, {})
        for t in types:
            if ch.get(t) is not False:
                failures.append(f"{channel}.{t} should be False")

    # Mobile and Slack: all types on
    for channel in ("mobile", "slack"):
        ch = ns.get(channel, {})
        for t in types:
            if ch.get(t) is not True:
                failures.append(f"{channel}.{t} should be True")

    if failures:
        return False, "; ".join(failures)
    return True, "All channels enabled with correct type configurations."
