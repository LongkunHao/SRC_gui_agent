# Task: Set email notification types to match desktop notification types.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    # Desktop seed values (these should not change):
    # assigned=T, statusChanged=T, commented=T, mentioned=T, projectUpdated=T, cycleUpdated=F
    # Email should now match desktop exactly.
    desktop = ns.get("desktop", {})
    email = ns.get("email", {})

    notif_types = ("issueAssigned", "issueStatusChanged", "issueCommented",
                   "issueMentioned", "projectUpdated", "cycleUpdated")

    for key in notif_types:
        desktop_val = desktop.get(key)
        email_val = email.get(key)
        if email_val != desktop_val:
            failures.append(f"email.{key} is {email_val}, should match desktop value {desktop_val}")

    if failures:
        return False, "; ".join(failures)
    return True, "Email notification types now match desktop notification types."
