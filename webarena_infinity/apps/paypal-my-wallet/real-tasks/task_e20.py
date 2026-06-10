import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    bank_accounts = state.get("bankAccounts")
    if bank_accounts is None:
        return False, "bankAccounts not found in state."

    for account in bank_accounts:
        if account.get("lastFour") == "1104":
            return False, "Citibank checking account (ending 1104) is still present in bankAccounts."

    return True, "Citibank checking account (ending 1104) has been deleted."
