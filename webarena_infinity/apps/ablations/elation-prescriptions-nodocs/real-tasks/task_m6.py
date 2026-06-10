import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rr_007 = next((rr for rr in state.get("refillRequests", []) if rr["id"] == "rr_007"), None)
    if rr_007 is None:
        return False, "Refill request rr_007 not found."

    if rr_007.get("status") != "denied":
        return False, f"Expected rr_007 status 'denied', got '{rr_007.get('status')}'."

    deny_reason = rr_007.get("denyReason", "")
    if not ("appointment" in deny_reason.lower() or "follow-up" in deny_reason.lower() or "follow up" in deny_reason.lower()):
        return False, f"Expected rr_007 denyReason to mention 'appointment' or 'follow-up', got '{deny_reason}'."

    return True, "William Thornton's Valsartan refill (rr_007) denied — needs appointment."
