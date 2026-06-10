import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    balances = state.get("balances")
    if balances is None:
        return False, "No balances found in state."

    cad_balances = [b for b in balances if b.get("currency") == "CAD"]
    if cad_balances:
        return False, f"Canadian dollars (CAD) still present in wallet with amount {cad_balances[0].get('amount')}."

    return True, "Canadian dollars (CAD) have been successfully removed from the wallet."
