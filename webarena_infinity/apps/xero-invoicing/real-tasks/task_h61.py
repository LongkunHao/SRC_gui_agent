import requests
from datetime import datetime, timedelta


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    today = datetime.strptime("2026-03-06", "%Y-%m-%d")
    cutoff = today - timedelta(days=14)

    invoices = state.get("invoices", [])

    # Find which invoices should be voided: awaiting_payment with due date before cutoff
    should_void = []
    should_not_void = []
    for inv in invoices:
        if inv.get("number") in ("INV-0045", "INV-0046", "INV-0047", "INV-0048",
                                  "INV-0049", "INV-0050", "INV-0051", "INV-0052",
                                  "INV-0053", "INV-0054", "INV-0055", "INV-0061", "INV-0062"):
            due = inv.get("dueDate", "")
            if not due:
                continue
            due_dt = datetime.strptime(due, "%Y-%m-%d")
            if due_dt < cutoff:
                should_void.append(inv)
            else:
                should_not_void.append(inv)

    # INV-0045 (due 2/19), INV-0046 (due 2/1), INV-0047 (due 2/15) should be voided
    voided_nums = []
    for inv in should_void:
        if inv.get("status") != "voided":
            return False, f"Expected {inv['number']} status 'voided', got '{inv.get('status')}'."
        voided_nums.append(inv["number"])

    if len(voided_nums) < 3:
        return False, f"Expected 3 invoices voided (>2 weeks overdue), found {len(voided_nums)}."

    # Invoices not overdue by >2 weeks should NOT be voided
    for inv in should_not_void:
        if inv.get("status") == "voided":
            return False, f"{inv['number']} should not be voided (not overdue >2 weeks)."

    return True, f"Voided {len(voided_nums)} invoices overdue >2 weeks: {', '.join(sorted(voided_nums))}."
