# Task: Configure all 4 notification channels to only notify for mentions.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    for channel in ("desktop", "mobile", "email", "slack"):
        ch = ns.get(channel, {})
        if not ch.get("enabled"):
            failures.append(f"{channel} should be enabled")
        for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                     "projectUpdated", "cycleUpdated"):
            if ch.get(key):
                failures.append(f"{channel}.{key} should be false")
        if not ch.get("issueMentioned"):
            failures.append(f"{channel}.issueMentioned should be true")

    if failures:
        return False, "; ".join(failures)
    return True, "All four channels enabled with only mentions notification type active."
