import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    bank_accounts = state.get("bankAccounts", [])

    # Check no bank with lastFour "1104" (Citibank checking)
    for bank in bank_accounts:
        if bank.get("lastFour") == "1104":
            errors.append(
                "Citibank checking account (lastFour '1104') still exists in bankAccounts."
            )
            break

    # Check no bank with lastFour "7823" (US Bank savings)
    for bank in bank_accounts:
        if bank.get("lastFour") == "7823":
            errors.append(
                "US Bank savings account (lastFour '7823') still exists in bankAccounts."
            )
            break

    if errors:
        return False, " ".join(errors)
    return True, "Successfully removed both Citibank checking and US Bank savings accounts."
