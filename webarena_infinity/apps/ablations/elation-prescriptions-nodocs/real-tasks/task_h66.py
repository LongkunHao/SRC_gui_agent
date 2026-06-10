import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Margaret's refills: approve if underlying rx has >=3 refills, deny if <3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rr_002 (Metformin, rx_003 had 3 refills) → approved
    rr_002 = next((r for r in state["refillRequests"] if r["id"] == "rr_002"), None)
    if not rr_002:
        errors.append("Refill request rr_002 not found.")
    elif rr_002.get("status") != "approved":
        errors.append(f"Expected rr_002 (Metformin) status 'approved', got '{rr_002.get('status')}'.")

    # rr_011 (Sertraline, rx_013 had 3 refills) → approved
    rr_011 = next((r for r in state["refillRequests"] if r["id"] == "rr_011"), None)
    if not rr_011:
        errors.append("Refill request rr_011 not found.")
    elif rr_011.get("status") != "approved":
        errors.append(f"Expected rr_011 (Sertraline) status 'approved', got '{rr_011.get('status')}'.")

    # rr_001 (Atorvastatin, rx_001 had 2 refills) → denied
    rr_001 = next((r for r in state["refillRequests"] if r["id"] == "rr_001"), None)
    if not rr_001:
        errors.append("Refill request rr_001 not found.")
    elif rr_001.get("status") != "denied":
        errors.append(f"Expected rr_001 (Atorvastatin) status 'denied', got '{rr_001.get('status')}'.")

    # rr_003 (Pantoprazole, rx_005 had 1 refill) → denied
    rr_003 = next((r for r in state["refillRequests"] if r["id"] == "rr_003"), None)
    if not rr_003:
        errors.append("Refill request rr_003 not found.")
    elif rr_003.get("status") != "denied":
        errors.append(f"Expected rr_003 (Pantoprazole) status 'denied', got '{rr_003.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Refill requests processed correctly based on underlying prescription refill counts."
