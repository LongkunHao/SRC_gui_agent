# Task: Invert all email notification type settings.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    email = state.get("notificationSettings", {}).get("email", {})
    failures = []

    # Seed: assigned=T, statusChanged=T, commented=F, mentioned=T, projectUpdated=F, cycleUpdated=F
    # After inversion: assigned=F, statusChanged=F, commented=T, mentioned=F, projectUpdated=T, cycleUpdated=T
    expected = {
        "issueAssigned": False,
        "issueStatusChanged": False,
        "issueCommented": True,
        "issueMentioned": False,
        "projectUpdated": True,
        "cycleUpdated": True,
    }

    for key, expected_val in expected.items():
        actual = email.get(key)
        if actual != expected_val:
            failures.append(f"email.{key}: expected {expected_val}, got {actual}")

    if failures:
        return False, "; ".join(failures)
    return True, "All email notification types inverted correctly."
