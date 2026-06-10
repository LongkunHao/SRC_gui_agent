# Task: Set username to local part of email, disable full name display.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Seed email: alex.morgan@acmecorp.io → local part: alex.morgan
    username = state.get("currentUser", {}).get("username", "")
    if username != "alex.morgan":
        failures.append(f"Expected username 'alex.morgan', got '{username}'")

    display_full = state.get("preferences", {}).get("displayFullNames")
    if display_full is not False:
        failures.append(f"displayFullNames should be false, got {display_full}")

    if failures:
        return False, "; ".join(failures)
    return True, "Username set to email local part and full name display disabled."
