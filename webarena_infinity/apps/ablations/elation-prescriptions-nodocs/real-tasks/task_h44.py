import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Most-filled active medication (Metformin): quantity 90 + pending refill approved."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_003 (Metformin, 4 fills — the most) -> quantity 90
    rx_003 = next((r for r in state["prescriptions"] if r["id"] == "rx_003"), None)
    if not rx_003:
        errors.append("Prescription rx_003 (Metformin) not found.")
    elif rx_003.get("quantity") != 90:
        errors.append(f"Expected rx_003 (Metformin) quantity 90, got {rx_003.get('quantity')}.")

    # rr_002 (Metformin pending refill) -> approved
    rr_002 = next((r for r in state["refillRequests"] if r["id"] == "rr_002"), None)
    if not rr_002:
        errors.append("Refill request rr_002 (Metformin) not found.")
    elif rr_002.get("status") != "approved":
        errors.append(f"Expected rr_002 (Metformin refill) status 'approved', got '{rr_002.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "Most-filled medication (Metformin) updated: quantity 90, refill approved."
