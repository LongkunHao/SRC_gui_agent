import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["displayFullNames"] == False:
        return True, "Display full names toggle correctly turned off."
    return False, f"Expected displayFullNames to be False, got {state['preferences']['displayFullNames']}."
