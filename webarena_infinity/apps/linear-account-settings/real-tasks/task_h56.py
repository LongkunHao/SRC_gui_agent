# Task: Enable Slack with opposite notification types of email channel.
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
        failures.append("Slack channel should be enabled")

    # Email seed: assigned=T, statusChanged=T, commented=F, mentioned=T, projectUpdated=F, cycleUpdated=F
    # Slack should be opposite: assigned=F, statusChanged=F, commented=T, mentioned=F, projectUpdated=T, cycleUpdated=T
    expected = {
        "issueAssigned": False, "issueStatusChanged": False, "issueCommented": True,
        "issueMentioned": False, "projectUpdated": True, "cycleUpdated": True
    }
    for key, val in expected.items():
        if slack.get(key) != val:
            failures.append(f"slack.{key} should be {val}, got {slack.get(key)}")

    if failures:
        return False, "; ".join(failures)
    return True, "Slack enabled with opposite notification types of email channel."
