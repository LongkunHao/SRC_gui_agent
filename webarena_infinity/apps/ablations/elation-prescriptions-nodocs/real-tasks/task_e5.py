import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    refill_requests = state.get("refillRequests", [])
    rr_002 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_002":
            rr_002 = rr
            break

    if rr_002 is None:
        return False, "Refill request rr_002 not found in state."

    rr_status = rr_002.get("status", "")
    if rr_status != "denied":
        return False, f"Expected rr_002 status to be 'denied', but got '{rr_status}'."

    deny_reason = rr_002.get("denyReason", "")
    if "lab" not in deny_reason.lower():
        return False, f"Expected rr_002 denyReason to contain 'lab' (case insensitive), but got '{deny_reason}'."

    return True, "Metformin refill (rr_002) denied with lab-related reason."
