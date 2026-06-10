import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find message msg_03 (Meta ML Engineer Intern)
    messages = state.get("messages", [])
    msg_03 = None
    for message in messages:
        if message.get("id") == "msg_03":
            msg_03 = message
            break

    if msg_03 is None:
        return False, "Message msg_03 (Meta ML Engineer Intern) not found in state."

    if not msg_03.get("isRead"):
        return False, f"Message msg_03 isRead is {msg_03.get('isRead')}, expected True."

    return True, "Successfully read the Meta ML Engineer Intern message. isRead=True."
