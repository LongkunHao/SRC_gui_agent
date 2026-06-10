import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    bank_accounts = state.get("bankAccounts", [])
    remaining_last_fours = {b.get("lastFour") for b in bank_accounts}

    # Confirmed bank accounts and lastUsed dates:
    # Chase 6742: 2026-03-01 (most recent)
    # BofA 3891: 2026-01-05
    # Citibank 1104: 2025-11-20
    # US Bank 7823: 2025-08-15 (least recently used)
    # Wells Fargo 5518: pending (not confirmed, should be ignored)

    # US Bank 7823 should be removed (least recently used confirmed)
    if "7823" in remaining_last_fours:
        errors.append("US Bank 7823 (least recently used confirmed account) should have been removed.")

    # All other accounts should remain
    for lf in ["6742", "3891", "1104", "5518"]:
        if lf not in remaining_last_fours:
            errors.append(f"Bank account ending in {lf} was removed but should have been kept.")

    if errors:
        return False, " ".join(errors)
    return True, "Removed US Bank 7823 (least recently used confirmed bank account)."
