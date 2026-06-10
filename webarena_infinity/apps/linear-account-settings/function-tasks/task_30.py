import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["onGitBranchCopyMoveToStarted"] == False:
        return True, "On git branch copy, move to started toggle correctly turned off."
    return False, f"Expected onGitBranchCopyMoveToStarted to be False, got {state['preferences']['onGitBranchCopyMoveToStarted']}."
