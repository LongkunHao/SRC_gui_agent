import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    banks = state.get("bankAccounts", [])

    for bank in banks:
        if bank.get("lastFour") == "1104":
            return False, "Citibank ****1104 still exists in bankAccounts."

    return True, "Citibank ****1104 has been removed."
