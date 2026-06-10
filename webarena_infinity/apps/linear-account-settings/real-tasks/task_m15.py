# Stop auto-assign behavior when copying a git branch name
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("onGitBranchCopyAutoAssign")
    if val is not False:
        return False, f"preferences.onGitBranchCopyAutoAssign is {val}, expected False"
    return True, "Auto-assign on git branch copy is disabled"
