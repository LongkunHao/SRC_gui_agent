import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # QU-0024 is the Atlas Engineering collaboration platform quote
    quo = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0024"), None)
    if quo is None:
        return False, "Quote QU-0024 not found."

    if quo.get("title") != "Engineering Hub Platform v2":
        return False, f"Expected title 'Engineering Hub Platform v2', got '{quo.get('title')}'."

    return True, "QU-0024 title updated to 'Engineering Hub Platform v2'."
