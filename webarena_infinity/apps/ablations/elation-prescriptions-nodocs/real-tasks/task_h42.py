import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Age-based refill processing: approve for patients over 75, deny the rest."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # William Thornton (pat_004, born 1944, age 81) — over 75, approve
    # rr_007 (Valsartan) -> approved
    rr_007 = next((r for r in state["refillRequests"] if r["id"] == "rr_007"), None)
    if not rr_007:
        errors.append("Refill request rr_007 not found.")
    elif rr_007.get("status") != "approved":
        errors.append(f"Expected rr_007 (Valsartan, William 81yo) status 'approved', got '{rr_007.get('status')}'.")

    # rr_010 (Furosemide) -> approved
    rr_010 = next((r for r in state["refillRequests"] if r["id"] == "rr_010"), None)
    if not rr_010:
        errors.append("Refill request rr_010 not found.")
    elif rr_010.get("status") != "approved":
        errors.append(f"Expected rr_010 (Furosemide, William 81yo) status 'approved', got '{rr_010.get('status')}'.")

    # Margaret Chen (pat_001, born 1958, age 67) — under 75, deny
    for rr_id, drug in [("rr_001", "Atorvastatin"), ("rr_002", "Metformin"),
                        ("rr_003", "Pantoprazole"), ("rr_011", "Sertraline")]:
        rr = next((r for r in state["refillRequests"] if r["id"] == rr_id), None)
        if not rr:
            errors.append(f"Refill request {rr_id} not found.")
        elif rr.get("status") != "denied":
            errors.append(f"Expected {rr_id} ({drug}, Margaret 67yo) status 'denied', got '{rr.get('status')}'.")

    # David Kowalski (pat_002, born 1975, age 50) — under 75, deny
    rr_005 = next((r for r in state["refillRequests"] if r["id"] == "rr_005"), None)
    if not rr_005:
        errors.append("Refill request rr_005 not found.")
    elif rr_005.get("status") != "denied":
        errors.append(f"Expected rr_005 (Metoprolol, David 50yo) status 'denied', got '{rr_005.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "All pending refills processed correctly by patient age."
