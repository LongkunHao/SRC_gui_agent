"""
Task: Read the Apple Pathways message.
Verify: msg_08 isRead == True.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    messages = state.get("messages", [])

    msg = next((m for m in messages if m.get("id") == "msg_08"), None)
    if msg is None:
        return False, "Message msg_08 (Apple Pathways) not found in messages list."

    if msg.get("isRead") != True:
        return False, (
            f"Message msg_08 (Apple Pathways) is not marked as read. "
            f"isRead={msg.get('isRead')}"
        )

    return True, "Apple Pathways message (msg_08) is marked as read."
