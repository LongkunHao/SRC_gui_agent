import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["openInDesktopApp"] == False:
        return True, "Open in desktop app toggle correctly turned off."
    return False, f"Expected openInDesktopApp to be False, got {state['preferences']['openInDesktopApp']}."
