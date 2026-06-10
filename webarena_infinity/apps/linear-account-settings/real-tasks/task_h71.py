# Task: Channel with most types on → mentions-only; channel with fewest types on → all-on.
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

    # Seed enabled channels type counts:
    #   desktop: 5 on (all except cycleUpdated) → MOST → mentions-only
    #   mobile: 4 on (assigned, status, commented, mentioned) → middle → unchanged
    #   email: 3 on (assigned, status, mentioned) → FEWEST → all-on

    # Desktop: mentions-only
    desktop = ns.get("desktop", {})
    expected_desktop = {"issueAssigned": False, "issueStatusChanged": False,
                        "issueCommented": False, "issueMentioned": True,
                        "projectUpdated": False, "cycleUpdated": False}
    for key, val in expected_desktop.items():
        if desktop.get(key) != val:
            failures.append(f"desktop.{key} should be {val}, got {desktop.get(key)}")

    # Email: all-on
    email = ns.get("email", {})
    for t in types:
        if email.get(t) is not True:
            failures.append(f"email.{t} should be True (fewest types channel → all-on)")

    # Mobile: unchanged from seed
    mobile = ns.get("mobile", {})
    expected_mobile = {"issueAssigned": True, "issueStatusChanged": True,
                       "issueCommented": True, "issueMentioned": True,
                       "projectUpdated": False, "cycleUpdated": False}
    for key, val in expected_mobile.items():
        if mobile.get(key) != val:
            failures.append(f"mobile.{key} should remain {val}, got {mobile.get(key)}")

    if failures:
        return False, "; ".join(failures)
    return True, "Desktop set to mentions-only and email set to all-on."
