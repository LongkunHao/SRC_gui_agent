import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    refill_requests = state.get("refillRequests", [])
    rr_011 = None
    for rr in refill_requests:
        if rr.get("id") == "rr_011":
            rr_011 = rr
            break

    if rr_011 is None:
        return False, "Refill request rr_011 not found in state."

    rr_status = rr_011.get("status", "")
    if rr_status != "denied":
        return False, f"Expected rr_011 status to be 'denied', but got '{rr_status}'."

    deny_reason = rr_011.get("denyReason", "")
    if "changed therapy" not in deny_reason.lower():
        return False, f"Expected rr_011 denyReason to contain 'changed therapy' (case insensitive), but got '{deny_reason}'."

    return True, "Sertraline refill (rr_011) denied with 'changed therapy' reason."
