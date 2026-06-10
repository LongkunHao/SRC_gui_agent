import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check refill request rr_001 status
    refill_requests = state.get("refillRequests", [])
    rr_001 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_001":
            rr_001 = rr
            break

    if rr_001 is None:
        return False, "Refill request rr_001 not found in state."

    rr_status = rr_001.get("status", "")
    if rr_status != "approved":
        return False, f"Expected rr_001 status to be 'approved', but got '{rr_status}'."

    responded_by = rr_001.get("respondedBy", "")
    if responded_by != "prov_001":
        return False, f"Expected rr_001 respondedBy to be 'prov_001', but got '{responded_by}'."

    # Check prescription rx_001 refillsRemaining
    prescriptions = state.get("prescriptions", [])
    rx_001 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_001":
            rx_001 = rx
            break

    if rx_001 is None:
        return False, "Prescription rx_001 (Atorvastatin) not found in state."

    refills_remaining = rx_001.get("refillsRemaining")
    if refills_remaining != 1:
        return False, f"Expected rx_001 refillsRemaining to be 1, but got {refills_remaining}."

    # Check fill history has at least 3 entries
    fill_history = rx_001.get("fillHistory", [])
    if len(fill_history) < 3:
        return False, f"Expected rx_001 fillHistory to have at least 3 entries, but got {len(fill_history)}."

    return True, "Atorvastatin refill (rr_001) approved successfully with updated fill history."
