import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard", {})
    daily_spending_limit = debit_card.get("dailySpendingLimit")

    if daily_spending_limit != 5000:
        return False, f"paypalDebitCard.dailySpendingLimit should be 5000, but got {daily_spending_limit}."

    return True, "Daily spending limit was successfully set to $5000."
