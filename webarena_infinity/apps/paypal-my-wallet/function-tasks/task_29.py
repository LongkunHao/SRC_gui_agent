import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard")
    if not debit_card:
        return False, "paypalDebitCard not found in state."

    cash_back = debit_card.get("cashBackCategory")
    if cash_back == "Groceries":
        return True, "Cash back category successfully changed to 'Groceries'."
    return False, f"Expected cashBackCategory to be 'Groceries', but got '{cash_back}'."
