import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    banks = state.get("bankAccounts", [])

    new_bank = None
    for bank in banks:
        if bank.get("lastFour") == "4455":
            new_bank = bank
            break

    if new_bank is None:
        return False, "No bank account with lastFour '4455' found."

    if new_bank.get("bankName") != "TD Bank":
        return False, f"Bank ****4455 bankName is '{new_bank.get('bankName')}', expected 'TD Bank'."

    if new_bank.get("accountType") != "checking":
        return False, f"Bank ****4455 accountType is '{new_bank.get('accountType')}', expected 'checking'."

    if new_bank.get("status") != "pending_confirmation":
        return False, f"Bank ****4455 status is '{new_bank.get('status')}', expected 'pending_confirmation'."

    return True, "TD Bank checking ****4455 has been added successfully."
