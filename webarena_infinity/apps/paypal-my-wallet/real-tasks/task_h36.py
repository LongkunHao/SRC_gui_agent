import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    debit = state.get("paypalDebitCard")
    if debit is None:
        return False, "No paypalDebitCard found in state."

    # Direct deposit employer should be "Apex Industries"
    dd = debit.get("directDeposit", {})
    employer = dd.get("employer", "")
    if employer != "Apex Industries":
        errors.append(
            f"Direct deposit employer is '{employer}', expected 'Apex Industries'."
        )

    # ATM limit should be 300
    atm_limit = debit.get("dailyATMLimit", 0)
    if atm_limit != 300:
        errors.append(
            f"Daily ATM limit is {atm_limit}, expected 300."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Direct deposit employer updated to Apex Industries and ATM limit set to $300."
