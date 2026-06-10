import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])
    mxn_balance = None
    for b in balances:
        if b.get("currency") == "MXN":
            mxn_balance = b
            break

    if mxn_balance is None:
        errors.append("No MXN (Mexican Peso) balance found in state['balances'].")
    else:
        if mxn_balance.get("amount") != 0:
            errors.append(
                f"MXN balance amount is {mxn_balance.get('amount')}, expected 0."
            )
        if mxn_balance.get("isPrimary") is not False:
            errors.append(
                f"MXN balance isPrimary is {mxn_balance.get('isPrimary')}, expected False."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Mexican Peso (MXN) currency successfully added with amount 0 and isPrimary False."
