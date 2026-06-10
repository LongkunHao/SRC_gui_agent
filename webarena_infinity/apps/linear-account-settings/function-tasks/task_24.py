import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["usePointerCursor"] == True:
        return True, "Use pointer cursor toggle correctly turned on."
    return False, f"Expected usePointerCursor to be True, got {state['preferences']['usePointerCursor']}."
