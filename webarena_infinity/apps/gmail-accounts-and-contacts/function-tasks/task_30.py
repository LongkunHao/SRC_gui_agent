import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    delegates = state.get("delegates", [])
    target_delegate = None
    for delegate in delegates:
        if delegate.get("email") == "assistant@company.com":
            target_delegate = delegate
            break

    if target_delegate is None:
        return False, "No delegate with email 'assistant@company.com' found."

    if target_delegate.get("name") != "Office Assistant":
        return False, f"Delegate name is '{target_delegate.get('name')}', expected 'Office Assistant'."

    if target_delegate.get("status") != "pending":
        return False, f"Delegate status is '{target_delegate.get('status')}', expected 'pending'."

    return True, "Delegate 'Office Assistant' (assistant@company.com) exists with status 'pending'."
