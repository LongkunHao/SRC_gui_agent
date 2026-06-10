# Task: Conditional per enabled channel: >3 types → comments+mentions only; ≤3 → all on.
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

    # Desktop seed: 5 types on (>3) → comments + mentions only
    desktop = ns.get("desktop", {})
    expected_desktop = {"issueAssigned": False, "issueStatusChanged": False,
                        "issueCommented": True, "issueMentioned": True,
                        "projectUpdated": False, "cycleUpdated": False}
    for key, val in expected_desktop.items():
        if desktop.get(key) != val:
            failures.append(f"desktop.{key} should be {val}, got {desktop.get(key)}")

    # Mobile seed: 4 types on (>3) → comments + mentions only
    mobile = ns.get("mobile", {})
    expected_mobile = {"issueAssigned": False, "issueStatusChanged": False,
                       "issueCommented": True, "issueMentioned": True,
                       "projectUpdated": False, "cycleUpdated": False}
    for key, val in expected_mobile.items():
        if mobile.get(key) != val:
            failures.append(f"mobile.{key} should be {val}, got {mobile.get(key)}")

    # Email seed: 3 types on (≤3) → all on
    email = ns.get("email", {})
    for t in types:
        if email.get(t) is not True:
            failures.append(f"email.{t} should be True (≤3 types → all on)")

    # Slack is disabled → should remain unchanged from seed
    slack = ns.get("slack", {})
    if slack.get("enabled") is not False:
        failures.append("slack should remain disabled (was not enabled)")
    seed_slack = {"issueAssigned": False, "issueStatusChanged": False,
                  "issueCommented": False, "issueMentioned": False,
                  "projectUpdated": False, "cycleUpdated": False}
    for key, val in seed_slack.items():
        if slack.get(key) != val:
            failures.append(f"slack.{key} should remain {val}")

    if failures:
        return False, "; ".join(failures)
    return True, "Conditional notification types applied correctly per channel."
