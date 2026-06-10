# Task: Show git attachments with the repository name and enable auto-assign when moving to started.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})
    git_format = prefs.get("gitAttachmentFormat", "")
    auto_assign = prefs.get("autoAssignOnStarted")
    errors = []
    if git_format != "Title and repository":
        errors.append(f"Expected gitAttachmentFormat 'Title and repository', got '{git_format}'")
    if auto_assign is not True:
        errors.append(f"Expected autoAssignOnStarted == True, got {auto_assign}")
    if errors:
        return False, "; ".join(errors)
    return True, "Git attachment format and auto-assign settings updated correctly."
