import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        return False, "No PayPal debit card found in state."

    direct_deposit = debit_card.get("directDeposit")
    if direct_deposit is None:
        return False, "No directDeposit section found in paypalDebitCard."

    employer = direct_deposit.get("employer")
    if employer != "Global Dynamics":
        return False, (
            f"Direct deposit employer is '{employer}', expected 'Global Dynamics'."
        )

    return True, "Direct deposit employer has been successfully updated to 'Global Dynamics'."
