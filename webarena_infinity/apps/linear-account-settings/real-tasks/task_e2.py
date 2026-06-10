# Task: Turn off the emoji conversion for text emoticons.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("convertTextEmojis")
    if val is False:
        return True, "convertTextEmojis is disabled."
    return False, f"Expected convertTextEmojis to be False, got {val}."
