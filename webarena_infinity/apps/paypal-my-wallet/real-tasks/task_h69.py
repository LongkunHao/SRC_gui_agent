import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check Apple gift card was purchased ($100, for self)
    gift_cards = state.get("giftCards", [])
    seed_gc_ids = {"gc_001", "gc_002", "gc_003", "gc_004", "gc_005"}
    new_apple_gcs = [
        gc for gc in gift_cards
        if gc.get("id") not in seed_gc_ids
        and gc.get("merchantName") == "Apple"
        and gc.get("amount") == 100
    ]
    if not new_apple_gcs:
        errors.append("No new $100 Apple gift card found.")
    else:
        gc = new_apple_gcs[0]
        user_email = state.get("currentUser", {}).get("email", "")
        if gc.get("recipientEmail") != user_email:
            errors.append(
                f"Apple gift card recipient is '{gc.get('recipientEmail')}', "
                f"expected '{user_email}' (self)."
            )

    # Check debit card cashback category is Fuel
    debit = state.get("paypalDebitCard", {})
    if debit.get("cashBackCategory") != "Fuel":
        errors.append(
            f"Debit card cashback category is '{debit.get('cashBackCategory')}', expected 'Fuel'."
        )

    # Check daily spending limit is 5000
    if debit.get("dailySpendingLimit") != 5000:
        errors.append(
            f"Debit card daily spending limit is {debit.get('dailySpendingLimit')}, expected 5000."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Bought $100 Apple gift card for self, set cashback to Fuel, spending limit to $5,000."
