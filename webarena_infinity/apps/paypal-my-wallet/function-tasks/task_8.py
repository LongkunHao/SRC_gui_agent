import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    banks = state.get("bankAccounts", [])

    target = None
    for bank in banks:
        if bank.get("lastFour") == "5518":
            target = bank
            break

    if target is None:
        return False, "Bank account with lastFour '5518' not found."

    if target.get("status") != "confirmed":
        return False, f"Bank ****5518 status is '{target.get('status')}', expected 'confirmed'."

    if target.get("confirmedAt") is None:
        return False, "Bank ****5518 confirmedAt is None, expected a timestamp."

    return True, "Wells Fargo ****5518 has been confirmed successfully."
