# Task: Disable spell check.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("enableSpellCheck")
    if val is False:
        return True, "Spell check is disabled"
    return False, f"enableSpellCheck is {val}, expected False"
