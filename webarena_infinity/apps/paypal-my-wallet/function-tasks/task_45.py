import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the bank account with bankName containing 'Chase' and lastFour '6742'
    banks = state.get("banks", state.get("bankAccounts", []))
    chase_bank = None
    for bank in banks:
        bank_name = bank.get("bankName", bank.get("name", ""))
        last_four = bank.get("lastFour", "")
        if "chase" in bank_name.lower() and last_four == "6742":
            chase_bank = bank
            break

    if chase_bank is None:
        return False, "Could not find a bank account with bankName containing 'Chase' and lastFour '6742'."

    chase_id = chase_bank.get("id", "")

    # Check walletPreferences.backupPaymentMethod
    prefs = state.get("walletPreferences", {})
    backup = prefs.get("backupPaymentMethod", "")
    if backup != chase_id:
        return False, f"Expected walletPreferences.backupPaymentMethod to be '{chase_id}', got '{backup}'."

    return True, "Backup payment method is correctly set to Chase ****6742."
