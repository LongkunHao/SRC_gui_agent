# Task: Disable git-related automations and switch git attachment format to repository name.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})

    checks = [
        (prefs.get("onGitBranchCopyMoveToStarted") is False, f"onGitBranchCopyMoveToStarted is {prefs.get('onGitBranchCopyMoveToStarted')}, expected False"),
        (prefs.get("onGitBranchCopyAutoAssign") is False, f"onGitBranchCopyAutoAssign is {prefs.get('onGitBranchCopyAutoAssign')}, expected False"),
        (prefs.get("gitAttachmentFormat") == "Title and repository", f"gitAttachmentFormat is '{prefs.get('gitAttachmentFormat')}', expected 'Title and repository'"),
    ]
    for passed, msg in checks:
        if not passed:
            return False, msg
    return True, "Git automation preferences updated correctly."
