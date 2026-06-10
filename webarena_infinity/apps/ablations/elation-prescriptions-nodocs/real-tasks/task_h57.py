import requests


def verify(server_url: str) -> tuple[bool, str]:
    """William's refills: approve cardiologist's, deny the other."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rr_010 (Furosemide, originally prescribed by Dr. Tanaka/cardiologist) -> approved
    rr_010 = next((r for r in state["refillRequests"] if r["id"] == "rr_010"), None)
    if not rr_010:
        errors.append("Refill request rr_010 not found.")
    elif rr_010.get("status") != "approved":
        errors.append(f"Expected rr_010 (Furosemide, cardiologist) status 'approved', got '{rr_010.get('status')}'.")

    # rr_007 (Valsartan, originally prescribed by Dr. Mitchell) -> denied
    rr_007 = next((r for r in state["refillRequests"] if r["id"] == "rr_007"), None)
    if not rr_007:
        errors.append("Refill request rr_007 not found.")
    elif rr_007.get("status") != "denied":
        errors.append(f"Expected rr_007 (Valsartan, non-cardiologist) status 'denied', got '{rr_007.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "William's refills processed correctly by prescriber specialty."
