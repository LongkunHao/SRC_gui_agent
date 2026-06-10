import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check savings balance decreased from 12450.82 to around 11450.82
    savings = state.get("savingsAccount", {})
    savings_balance = savings.get("balance", 0)
    expected_savings = 12450.82 - 1000
    if abs(savings_balance - expected_savings) > 5.0:
        return False, f"savingsAccount.balance should be around {expected_savings}, but is {savings_balance}."

    # Check USD balance increased from 2847.63 to around 3847.63
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b
            break

    if usd_balance is None:
        return False, "No USD balance entry found."

    usd_amount = usd_balance.get("amount", 0)
    expected_usd = 2847.63 + 1000
    if abs(usd_amount - expected_usd) > 5.0:
        return False, f"USD balance should be around {expected_usd}, but is {usd_amount}."

    # Check savingsAccount.transferHistory has a new withdrawal entry with amount 1000
    transfer_history = savings.get("transferHistory", [])
    found_withdrawal = False
    for entry in transfer_history:
        if entry.get("type") == "withdrawal" and entry.get("amount") == 1000:
            found_withdrawal = True
            break

    if not found_withdrawal:
        return False, "No entry with type 'withdrawal' and amount 1000 found in savingsAccount.transferHistory."

    # Check for savings_withdrawal transaction
    transactions = state.get("transactions", [])
    found_savings_tx = False
    for t in transactions:
        if t.get("type") == "savings_withdrawal":
            found_savings_tx = True
            break

    if not found_savings_tx:
        return False, "No transaction with type 'savings_withdrawal' found."

    return True, "Successfully withdrew $1000 from savings. Savings balance decreased, USD increased, and transactions recorded."
