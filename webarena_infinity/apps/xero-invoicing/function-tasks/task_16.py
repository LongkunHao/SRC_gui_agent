import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0025"), None)
    if not quo:
        return False, "Quote QU-0025 not found."

    if quo["status"] != "sent":
        return False, f"Quote QU-0025 status is '{quo['status']}', expected 'sent'."

    if not quo.get("sentAt"):
        return False, "Quote QU-0025 sentAt is not set."

    return True, "Quote QU-0025 sent successfully."
