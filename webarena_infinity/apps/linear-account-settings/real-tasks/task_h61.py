# Task: Set username to URL key of workspace with most members, first day of week to sign-in day.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Most members: Open Source Collective (124) → urlKey "osc"
    username = state.get("currentUser", {}).get("username", "")
    if username != "osc":
        failures.append(f"Expected username 'osc', got '{username}'")

    # Current session signed in 2026-02-01 = Sunday
    first_day = state.get("preferences", {}).get("firstDayOfWeek", "")
    if first_day != "Sunday":
        failures.append(f"Expected firstDayOfWeek 'Sunday', got '{first_day}'")

    if failures:
        return False, "; ".join(failures)
    return True, "Username set to 'osc' and first day of week set to Sunday."
