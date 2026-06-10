import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0025"), None)
    if not quo:
        return False, "Quote QU-0025 not found."

    if quo["title"] != "Online Catering Portal":
        return False, f"Quote QU-0025 title is '{quo['title']}', expected 'Online Catering Portal'."

    return True, "Quote QU-0025 title updated to 'Online Catering Portal'."
