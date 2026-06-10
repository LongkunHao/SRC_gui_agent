"""Verify: Enable late penalty 5% daily, update notes on Metro Print draft invoices."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    settings = state.get("settings", {})
    errors = []

    # Settings checks
    if not settings.get("latePenaltyEnabled"):
        errors.append("latePenaltyEnabled is not True")
    if abs(settings.get("latePenaltyRate", 0) - 5) > 0.01:
        errors.append(f"latePenaltyRate is {settings.get('latePenaltyRate')}, expected 5")
    if settings.get("latePenaltyFrequency") != "daily":
        errors.append(f"latePenaltyFrequency is '{settings.get('latePenaltyFrequency')}', expected 'daily'")

    # Metro Print Solutions (con_8) draft invoices: inv_83, inv_108
    expected_notes = "Late penalty terms: 5% daily surcharge applies"
    for inv_id in ["inv_83", "inv_108"]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv.get("notes") != expected_notes:
            errors.append(f"{inv_id} notes is '{inv.get('notes')}', expected '{expected_notes}'")

    if errors:
        return False, "; ".join(errors)
    return True, "Late penalty 5% daily enabled; Metro Print draft notes updated"
