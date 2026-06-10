"""Verify: Company tax ID + late penalties updated, overdue < $5K voided."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings
    if settings.get("companyTaxId") != "NZ-99-999-999":
        errors.append(f"companyTaxId is '{settings.get('companyTaxId')}', expected 'NZ-99-999-999'")
    if not settings.get("latePenaltyEnabled"):
        errors.append("latePenaltyEnabled is False, expected True")
    if abs(settings.get("latePenaltyRate", 0) - 4) > 0.01:
        errors.append(f"latePenaltyRate is {settings.get('latePenaltyRate')}, expected 4")
    if settings.get("latePenaltyFrequency") != "daily":
        errors.append(f"latePenaltyFrequency is '{settings.get('latePenaltyFrequency')}', expected 'daily'")

    # Overdue invoices with total < $5,000 should be voided
    voided_targets = [
        ("inv_39", "INV-0039", 4027.5),
        ("inv_68", "INV-0068", 431.25),
        ("inv_87", "INV-0087", 690),
        ("inv_107", "INV-0107", 3392.5),
    ]
    for inv_id, inv_num, total in voided_targets:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        if inv["status"] != "voided":
            errors.append(f"{inv_num} (total ${total}) status is '{inv['status']}', expected 'voided'")
        if not inv.get("voidedAt"):
            errors.append(f"{inv_num} voidedAt is null")

    # Overdue invoices >= $5,000 should NOT be voided
    not_voided = [
        ("inv_15", "INV-0015"), ("inv_33", "INV-0033"), ("inv_40", "INV-0040"),
        ("inv_59", "INV-0059"), ("inv_63", "INV-0063"), ("inv_79", "INV-0079"),
        ("inv_89", "INV-0089"), ("inv_100", "INV-0100"), ("inv_102", "INV-0102"),
        ("inv_104", "INV-0104"),
    ]
    for inv_id, inv_num in not_voided:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if inv and inv["status"] == "voided":
            errors.append(f"{inv_num} was voided but should NOT have been (total >= $5,000)")

    if errors:
        return False, "; ".join(errors)
    return True, "Settings updated; overdue invoices < $5K voided"
