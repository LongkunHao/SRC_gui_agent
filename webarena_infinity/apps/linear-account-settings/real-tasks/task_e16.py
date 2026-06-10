# Task: Set Sunday as the first day of the week.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    val = state.get("preferences", {}).get("firstDayOfWeek")
    if val == "Sunday":
        return True, "First day of the week is set to Sunday"
    return False, f"firstDayOfWeek is '{val}', expected 'Sunday'"
