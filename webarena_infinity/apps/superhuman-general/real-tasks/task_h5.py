import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the Morning Brew email (id 38)
    morning_brew = None
    for e in state.get("emails", []):
        if e["id"] == 38:
            morning_brew = e
            break
    if not morning_brew:
        return False, "Morning Brew email (id 38) not found."

    # Check it's marked as done (unsubscribe archives the email)
    if not morning_brew.get("isDone", False):
        return False, "Morning Brew email is not archived (isDone is not true)."

    # Check crew@morningbrew.com is in blocked senders
    blocked_senders = state.get("settings", {}).get("blockedSenders", [])
    if "crew@morningbrew.com" not in blocked_senders:
        return False, f"'crew@morningbrew.com' not found in blocked senders. Current blocked: {blocked_senders}."

    return True, "Successfully unsubscribed from Morning Brew (email archived and sender blocked)."
