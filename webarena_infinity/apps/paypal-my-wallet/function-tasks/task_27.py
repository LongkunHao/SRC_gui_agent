import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard", {})
    direct_deposit = debit_card.get("directDeposit", {})
    employer = direct_deposit.get("employer")

    if employer != "Acme Corp":
        return False, f"paypalDebitCard.directDeposit.employer should be 'Acme Corp', but got '{employer}'."

    return True, "Employer was successfully changed to 'Acme Corp'."
