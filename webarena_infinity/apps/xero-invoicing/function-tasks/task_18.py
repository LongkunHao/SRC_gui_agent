import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0028"), None)
    if not quo:
        return False, "Quote QU-0028 not found."

    if quo["status"] != "declined":
        return False, f"Quote QU-0028 status is '{quo['status']}', expected 'declined'."

    return True, "Quote QU-0028 marked as declined."
