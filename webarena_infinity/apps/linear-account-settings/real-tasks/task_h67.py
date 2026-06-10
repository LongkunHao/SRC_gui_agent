# Task: Disconnect account linked same day as account creation, home view to last alphabetically.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Account created 2024-06-15, Google connected 2024-06-15 → disconnect Google
    accounts = state.get("connectedAccounts", [])
    providers = [a.get("provider") for a in accounts]
    if "Google" in providers:
        failures.append("Google account should have been disconnected (linked same day as account creation)")

    # Home view options alphabetically: Active issues, All issues, Current cycle,
    # Favorited Projects, Favorited Views, Inbox, My Issues → last = My Issues
    home = state.get("preferences", {}).get("defaultHomeView", "")
    if home != "My Issues":
        failures.append(f"Expected home view 'My Issues' (last alphabetically), got '{home}'")

    if failures:
        return False, "; ".join(failures)
    return True, "Google disconnected and home view set to My Issues."
