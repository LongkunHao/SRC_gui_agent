import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["firstDayOfWeek"]
    if val == "Wednesday":
        return True, "First day of week successfully changed to 'Wednesday'."
    return False, f"Expected firstDayOfWeek 'Wednesday', got '{val}'."
