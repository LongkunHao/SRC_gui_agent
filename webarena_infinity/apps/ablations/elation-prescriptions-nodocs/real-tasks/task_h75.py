import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Morning prep: 3 different refill actions + settings changes."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rr_003 (Pantoprazole, urgent) → approved
    rr_003 = next((r for r in state["refillRequests"] if r["id"] == "rr_003"), None)
    if not rr_003:
        errors.append("Refill request rr_003 not found.")
    elif rr_003.get("status") != "approved":
        errors.append(f"Expected rr_003 (Pantoprazole) status 'approved', got '{rr_003.get('status')}'.")

    # rr_002 (Metformin) → modified
    rr_002 = next((r for r in state["refillRequests"] if r["id"] == "rr_002"), None)
    if not rr_002:
        errors.append("Refill request rr_002 not found.")
    elif rr_002.get("status") != "modified":
        errors.append(f"Expected rr_002 (Metformin) status 'modified', got '{rr_002.get('status')}'.")
    elif not rr_002.get("modifiedDetails"):
        errors.append("Expected rr_002 to have modifiedDetails.")

    # rr_011 (Sertraline) → denied
    rr_011 = next((r for r in state["refillRequests"] if r["id"] == "rr_011"), None)
    if not rr_011:
        errors.append("Refill request rr_011 not found.")
    elif rr_011.get("status") != "denied":
        errors.append(f"Expected rr_011 (Sertraline) status 'denied', got '{rr_011.get('status')}'.")

    # rr_001 (Atorvastatin) → should remain pending
    rr_001 = next((r for r in state["refillRequests"] if r["id"] == "rr_001"), None)
    if rr_001 and rr_001.get("status") != "pending":
        errors.append(f"Expected rr_001 (Atorvastatin) to remain 'pending', got '{rr_001.get('status')}'.")

    # Settings
    settings = state.get("settings", {})
    if settings.get("defaultPharmacy") != "pharm_002":
        errors.append(f"Expected defaultPharmacy 'pharm_002' (Walgreens), got '{settings.get('defaultPharmacy')}'.")
    if settings.get("signatureRequired") is not False:
        errors.append(f"Expected signatureRequired False, got {settings.get('signatureRequired')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Morning clinic prep completed — refills processed and settings updated."
