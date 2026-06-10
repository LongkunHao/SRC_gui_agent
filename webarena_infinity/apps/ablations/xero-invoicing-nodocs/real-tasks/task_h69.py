"""Verify: $500 partial payment on every PROJ- overdue invoice via Business Savings."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # PROJ- overdue invoices: inv_39, inv_63, inv_87, inv_89
    targets = [
        ("inv_39", "INV-0039", "PROJ-GAMMA"),
        ("inv_63", "INV-0063", "PROJ-BETA"),
        ("inv_87", "INV-0087", "PROJ-ALPHA"),
        ("inv_89", "INV-0089", "PROJ-GAMMA"),
    ]
    for inv_id, inv_num, ref in targets:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} ({ref}) not found")
            continue
        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        new_pays = [p for p in inv_pays if abs(p.get("amount", 0) - 500) < 0.01]
        if not new_pays:
            errors.append(f"No $500 payment found for {inv_num}")
        else:
            pay = new_pays[-1]
            if pay.get("bankAccountId") != "bank_2":
                errors.append(f"{inv_num} payment uses '{pay.get('bankAccountId')}', expected 'bank_2' (Business Savings)")

    if errors:
        return False, "; ".join(errors)
    return True, "$500 partial payments on all PROJ- overdue invoices via Business Savings"
