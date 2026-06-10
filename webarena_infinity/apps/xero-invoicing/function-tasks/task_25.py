import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    cn = next((c for c in state["creditNotes"] if c["number"] == "CN-0011"), None)
    if not cn:
        return False, "Credit note CN-0011 not found."

    if cn["status"] != "awaiting_payment":
        return False, f"Credit note CN-0011 status is '{cn['status']}', expected 'awaiting_payment'."

    return True, "Credit note CN-0011 approved (status is awaiting_payment)."
