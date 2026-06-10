import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        return False, "No PayPal debit card found in state."

    daily_limit = debit_card.get("dailySpendingLimit")
    if daily_limit != 5000:
        return False, (
            f"Debit card dailySpendingLimit is {daily_limit}, expected 5000."
        )

    return True, "Debit card daily spending limit successfully raised to $5,000."
