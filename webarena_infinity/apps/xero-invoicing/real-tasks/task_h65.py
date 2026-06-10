import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Least expensive sent quote: QU-0028 ($14,410) -> should be declined
    qu_0028 = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0028"), None)
    if qu_0028 is None:
        return False, "QU-0028 not found."
    if qu_0028.get("status") != "declined":
        return False, f"Expected QU-0028 (least expensive sent) status 'declined', got '{qu_0028.get('status')}'."

    # Most expensive sent quote: QU-0024 ($76,725) -> should be accepted
    qu_0024 = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0024"), None)
    if qu_0024 is None:
        return False, "QU-0024 not found."
    if qu_0024.get("status") != "accepted":
        return False, f"Expected QU-0024 (most expensive sent) status 'accepted', got '{qu_0024.get('status')}'."

    return True, "QU-0028 declined (least expensive sent), QU-0024 accepted (most expensive sent)."
