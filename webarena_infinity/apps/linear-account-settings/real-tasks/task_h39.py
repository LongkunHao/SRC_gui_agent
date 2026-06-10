# Task: Maximum notifications — all channels enabled, all types on, all comms subscribed.
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

    for channel in ("desktop", "mobile", "email", "slack"):
        ch = ns.get(channel, {})
        if not ch.get("enabled"):
            failures.append(f"{channel} should be enabled")
        for key in notif_types:
            if not ch.get(key):
                failures.append(f"{channel}.{key} should be true")

    if not ns.get("receiveChangelogs"):
        failures.append("receiveChangelogs should be true")
    if not ns.get("receiveDpaUpdates"):
        failures.append("receiveDpaUpdates should be true")
    if not ns.get("receiveProductUpdates"):
        failures.append("receiveProductUpdates should be true")

    if failures:
        return False, "; ".join(failures)
    return True, "Maximum notifications configured: all channels, types, and communications enabled."
