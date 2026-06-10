import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    paypal_debit = state.get("paypalDebitCard")
    if paypal_debit is None:
        return False, "paypalDebitCard not found in state."

    direct_deposit = paypal_debit.get("directDeposit")
    if direct_deposit is None:
        return False, "directDeposit not found in paypalDebitCard."

    if direct_deposit.get("enabled") is not False:
        return False, f"Direct deposit is still enabled (enabled={direct_deposit.get('enabled')})."

    return True, "Direct deposit on debit card has been disabled."
