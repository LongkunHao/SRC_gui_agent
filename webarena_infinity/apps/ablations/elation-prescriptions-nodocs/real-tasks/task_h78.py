import requests


def verify(server_url: str) -> tuple[bool, str]:
    """End-of-week: settings + favorites + William refill/renew + Jessica discontinue."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # Settings
    settings = state.get("settings", {})
    if settings.get("printFormat") != "compact":
        errors.append(f"Expected printFormat 'compact', got '{settings.get('printFormat')}'.")
    if settings.get("defaultRefills") != 3:
        errors.append(f"Expected defaultRefills 3, got {settings.get('defaultRefills')}.")

    # Prednisone removed from favorites
    favs = settings.get("favoritesDrugIds", [])
    if "drug_045" in favs:
        errors.append("Prednisone (drug_045) still in favorites.")

    # rr_010 (William's Furosemide) → approved
    rr_010 = next((r for r in state["refillRequests"] if r["id"] == "rr_010"), None)
    if not rr_010:
        errors.append("Refill request rr_010 not found.")
    elif rr_010.get("status") != "approved":
        errors.append(f"Expected rr_010 (Furosemide) status 'approved', got '{rr_010.get('status')}'.")

    # William's Valsartan renewed with 5
    rx_022 = next((r for r in state["prescriptions"] if r["id"] == "rx_022"), None)
    if not rx_022:
        errors.append("Prescription rx_022 (Valsartan) not found.")
    elif rx_022.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_022 (Valsartan) refillsRemaining >= 5, got {rx_022.get('refillsRemaining')}.")

    # rx_025 (Jessica's Cephalexin) → discontinued
    rx_025 = next((r for r in state["prescriptions"] if r["id"] == "rx_025"), None)
    if not rx_025:
        errors.append("Prescription rx_025 (Cephalexin) not found.")
    elif rx_025.get("status") != "discontinued":
        errors.append(f"Expected rx_025 (Cephalexin) status 'discontinued', got '{rx_025.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "End-of-week tasks completed — settings, favorites, refill, and discontinuation."
