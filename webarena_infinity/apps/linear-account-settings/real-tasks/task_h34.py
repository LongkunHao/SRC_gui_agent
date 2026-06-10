# Task: Enable Slack with all 6 notification types, disable email channel.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    slack = ns.get("slack", {})
    if not slack.get("enabled"):
        failures.append("Slack notifications should be enabled")

    for key in ("issueAssigned", "issueStatusChanged", "issueCommented",
                "issueMentioned", "projectUpdated", "cycleUpdated"):
        if not slack.get(key):
            failures.append(f"slack.{key} should be true")

    email = ns.get("email", {})
    if email.get("enabled") is not False:
        failures.append("Email notification channel should be disabled")

    if failures:
        return False, "; ".join(failures)
    return True, "Slack fully enabled with all types; email channel disabled."
