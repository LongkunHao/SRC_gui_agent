# Task: Update email to match Google connected account's email, then disconnect Google.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    email = state.get("currentUser", {}).get("email", "")
    if email != "alex.morgan@gmail.com":
        failures.append(f"Expected email 'alex.morgan@gmail.com', got '{email}'")

    accounts = state.get("connectedAccounts", [])
    google_accounts = [a for a in accounts if a.get("provider") == "Google"]
    if google_accounts:
        failures.append("Google account still connected")

    if failures:
        return False, "; ".join(failures)
    return True, "Email updated to Google account's email and Google disconnected."
