import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    target_email = "support@vercel.com"

    other_contacts = state.get("otherContacts", [])
    for oc in other_contacts:
        if oc.get("email") == target_email:
            return False, f"Other contact with email '{target_email}' still exists in otherContacts."

    return True, f"No other contact with email '{target_email}' in otherContacts."
