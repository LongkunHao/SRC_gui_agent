import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quotes = state.get("quotes", [])

    # Sent quotes under $20k in seed: QU-0023 ($18,780), QU-0028 ($14,410)
    # Sent quote over $20k: QU-0024 ($76,725) should remain sent
    for num in ["QU-0023", "QU-0028"]:
        quo = next((q for q in quotes if q.get("number") == num), None)
        if quo is None:
            return False, f"Quote {num} not found."
        if quo.get("status") != "declined":
            return False, f"Expected {num} status 'declined', got '{quo.get('status')}'."

    # QU-0024 should still be sent
    qu24 = next((q for q in quotes if q.get("number") == "QU-0024"), None)
    if qu24 is None:
        return False, "Quote QU-0024 not found."
    if qu24.get("status") != "sent":
        return False, f"Expected QU-0024 to remain 'sent', got '{qu24.get('status')}'."

    return True, "QU-0023 and QU-0028 declined; QU-0024 unchanged."
