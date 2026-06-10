# Task: Full name = 'Alex Morgan (Admin)', home view = All issues, display full names = false.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    full_name = state.get("currentUser", {}).get("fullName", "")
    if full_name != "Alex Morgan (Admin)":
        failures.append(f"Expected full name 'Alex Morgan (Admin)', got '{full_name}'")

    home_view = state.get("preferences", {}).get("defaultHomeView")
    if home_view != "All issues":
        failures.append(f"Expected home view 'All issues', got '{home_view}'")

    display = state.get("preferences", {}).get("displayFullNames")
    if display is not False:
        failures.append(f"displayFullNames should be false, got {display}")

    if failures:
        return False, "; ".join(failures)
    return True, "Full name updated with role, home view set, display full names disabled."
