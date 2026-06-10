import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check savings balance increased from 12450.82 to around 12950.82
    savings = state.get("savingsAccount", {})
    savings_balance = savings.get("balance", 0)
    expected_savings = 12450.82 + 500
    if abs(savings_balance - expected_savings) > 5.0:
        return False, f"savingsAccount.balance should be around {expected_savings}, but is {savings_balance}."

    # Check USD balance decreased from 2847.63 to around 2347.63
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b
            break

    if usd_balance is None:
        return False, "No USD balance entry found."

    usd_amount = usd_balance.get("amount", 0)
    expected_usd = 2847.63 - 500
    if abs(usd_amount - expected_usd) > 5.0:
        return False, f"USD balance should be around {expected_usd}, but is {usd_amount}."

    # Check savingsAccount.transferHistory has a new deposit entry with amount 500
    transfer_history = savings.get("transferHistory", [])
    found_deposit = False
    for entry in transfer_history:
        if entry.get("type") == "deposit" and entry.get("amount") == 500:
            found_deposit = True
            break

    if not found_deposit:
        return False, "No entry with type 'deposit' and amount 500 found in savingsAccount.transferHistory."

    # Check for savings_deposit transaction
    transactions = state.get("transactions", [])
    found_savings_tx = False
    for t in transactions:
        if t.get("type") == "savings_deposit":
            found_savings_tx = True
            break

    if not found_savings_tx:
        return False, "No transaction with type 'savings_deposit' found."

    return True, "Successfully deposited $500 to savings. Savings balance increased, USD decreased, and transactions recorded."
