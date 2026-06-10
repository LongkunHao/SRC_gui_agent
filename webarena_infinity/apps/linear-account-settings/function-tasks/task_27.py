import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["enableSpellCheck"] == False:
        return True, "Spell check toggle correctly turned off."
    return False, f"Expected enableSpellCheck to be False, got {state['preferences']['enableSpellCheck']}."
