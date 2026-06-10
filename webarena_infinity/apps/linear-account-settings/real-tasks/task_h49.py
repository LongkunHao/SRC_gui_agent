# Task: Invert notification types for both mobile and desktop channels.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    # Desktop seed: assigned=T, statusChanged=T, commented=T, mentioned=T, projectUpdated=T, cycleUpdated=F
    # After invert: assigned=F, statusChanged=F, commented=F, mentioned=F, projectUpdated=F, cycleUpdated=T
    desktop = ns.get("desktop", {})
    expected_desktop = {
        "issueAssigned": False, "issueStatusChanged": False, "issueCommented": False,
        "issueMentioned": False, "projectUpdated": False, "cycleUpdated": True
    }
    for key, val in expected_desktop.items():
        if desktop.get(key) != val:
            failures.append(f"desktop.{key} should be {val}, got {desktop.get(key)}")

    # Mobile seed: assigned=T, statusChanged=T, commented=T, mentioned=T, projectUpdated=F, cycleUpdated=F
    # After invert: assigned=F, statusChanged=F, commented=F, mentioned=F, projectUpdated=T, cycleUpdated=T
    mobile = ns.get("mobile", {})
    expected_mobile = {
        "issueAssigned": False, "issueStatusChanged": False, "issueCommented": False,
        "issueMentioned": False, "projectUpdated": True, "cycleUpdated": True
    }
    for key, val in expected_mobile.items():
        if mobile.get(key) != val:
            failures.append(f"mobile.{key} should be {val}, got {mobile.get(key)}")

    if failures:
        return False, "; ".join(failures)
    return True, "Desktop and mobile notification types inverted correctly."
