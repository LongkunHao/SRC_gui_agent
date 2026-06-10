# Task: Enable all notification types for desktop notifications, including cycle updates.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    desktop = state.get("notificationSettings", {}).get("desktop", {})

    fields = [
        "enabled", "issueAssigned", "issueStatusChanged",
        "issueCommented", "issueMentioned", "projectUpdated", "cycleUpdated",
    ]

    failures = []
    for field in fields:
        val = desktop.get(field)
        if val != True:
            failures.append(f"desktop.{field}: expected True, got {val}")

    if failures:
        return False, "; ".join(failures)
    return True, "All desktop notification types enabled."
