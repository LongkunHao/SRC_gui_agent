import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # TechVault has two invoices: INV-0043 (2025-12-20, paid) and INV-0055 (2026-02-25)
    # The one issued before 2026 is INV-0043
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0043"), None)
    if inv is None:
        return False, "INV-0043 not found."

    if inv.get("status") != "voided":
        return False, f"Expected INV-0043 status 'voided', got '{inv.get('status')}'."

    # Ensure INV-0055 is NOT voided (disambiguation check)
    inv_055 = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0055"), None)
    if inv_055 and inv_055.get("status") == "voided":
        return False, "INV-0055 was voided but it was issued in 2026 — wrong invoice targeted."

    return True, "INV-0043 (TechVault, pre-2026) voided correctly."
