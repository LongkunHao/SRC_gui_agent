import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0025"), None)
    if not quo:
        return False, "Quote QU-0025 not found."

    if quo["expiryDate"] != "2026-04-30":
        return False, f"Quote QU-0025 expiry date is '{quo['expiryDate']}', expected '2026-04-30'."

    return True, "Quote QU-0025 expiry date updated to 2026-04-30."
