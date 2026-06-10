import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check refill request rr_010 status
    refill_requests = state.get("refillRequests", [])
    rr_010 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_010":
            rr_010 = rr
            break

    if rr_010 is None:
        return False, "Refill request rr_010 not found in state."

    rr_status = rr_010.get("status", "")
    if rr_status != "approved":
        return False, f"Expected rr_010 status to be 'approved', but got '{rr_status}'."

    # Check prescription rx_024 refillsRemaining
    prescriptions = state.get("prescriptions", [])
    rx_024 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_024":
            rx_024 = rx
            break

    if rx_024 is None:
        return False, "Prescription rx_024 (Furosemide) not found in state."

    refills_remaining = rx_024.get("refillsRemaining")
    if refills_remaining != 3:
        return False, f"Expected rx_024 refillsRemaining to be 3, but got {refills_remaining}."

    # Check fill history has at least 2 entries
    fill_history = rx_024.get("fillHistory", [])
    if len(fill_history) < 2:
        return False, f"Expected rx_024 fillHistory to have at least 2 entries, but got {len(fill_history)}."

    return True, "Furosemide refill (rr_010) approved with updated refills and fill history."
