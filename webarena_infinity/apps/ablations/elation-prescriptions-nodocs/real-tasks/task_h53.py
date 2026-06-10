import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Conditional refill processing: approve urgent, deny routine with fewest refills."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rr_003 (Pantoprazole, urgent) -> approved
    rr_003 = next((r for r in state["refillRequests"] if r["id"] == "rr_003"), None)
    if not rr_003:
        errors.append("Refill request rr_003 not found.")
    elif rr_003.get("status") != "approved":
        errors.append(f"Expected rr_003 (Pantoprazole, urgent) status 'approved', got '{rr_003.get('status')}'.")

    # rr_001 (Atorvastatin, routine, underlying rx has 2 refills — fewest) -> denied
    rr_001 = next((r for r in state["refillRequests"] if r["id"] == "rr_001"), None)
    if not rr_001:
        errors.append("Refill request rr_001 not found.")
    elif rr_001.get("status") != "denied":
        errors.append(f"Expected rr_001 (Atorvastatin, 2 refills remaining — fewest) status 'denied', got '{rr_001.get('status')}'.")

    # rr_002 (Metformin) -> still pending
    rr_002 = next((r for r in state["refillRequests"] if r["id"] == "rr_002"), None)
    if not rr_002:
        errors.append("Refill request rr_002 not found.")
    elif rr_002.get("status") != "pending":
        errors.append(f"Expected rr_002 (Metformin) status 'pending', got '{rr_002.get('status')}'.")

    # rr_011 (Sertraline) -> still pending
    rr_011 = next((r for r in state["refillRequests"] if r["id"] == "rr_011"), None)
    if not rr_011:
        errors.append("Refill request rr_011 not found.")
    elif rr_011.get("status") != "pending":
        errors.append(f"Expected rr_011 (Sertraline) status 'pending', got '{rr_011.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Refills processed correctly: urgent approved, fewest-refills routine denied, others pending."
