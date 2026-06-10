import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    refill_requests = state.get("refillRequests", [])
    permanent_rx = state.get("permanentRxMeds", [])

    # Gabapentin refill: approved with refills=5
    gaba_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_rr = r
            break
    if gaba_rr is None:
        return False, "Gabapentin refill request not found"
    if gaba_rr.get("status") != "approved":
        return False, f"Gabapentin refill status is '{gaba_rr.get('status')}', expected 'approved'"
    mods = gaba_rr.get("modifications", {})
    if mods.get("refills") != 5:
        return False, f"Gabapentin modifications.refills is {mods.get('refills')}, expected 5"

    # Gabapentin med should reflect updated refills
    gaba_med = None
    for m in permanent_rx:
        if m.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_med = m
            break
    if gaba_med and gaba_med.get("refillsRemaining") != 5:
        return False, f"Gabapentin refillsRemaining is {gaba_med.get('refillsRemaining')}, expected 5"

    # Omeprazole refill: approved with sig change
    omep_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Omeprazole 20mg capsule":
            omep_rr = r
            break
    if omep_rr is None:
        return False, "Omeprazole refill request not found"
    if omep_rr.get("status") != "approved":
        return False, f"Omeprazole refill status is '{omep_rr.get('status')}', expected 'approved'"
    omep_mods = omep_rr.get("modifications", {})
    omep_sig = omep_mods.get("sig", "").lower()
    if "twice daily" not in omep_sig and "bid" not in omep_sig:
        return False, f"Omeprazole modification sig should include 'twice daily', got: '{omep_mods.get('sig')}'"

    # Sertraline refill: denied with taper-related reason
    sert_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Sertraline 50mg tablet":
            sert_rr = r
            break
    if sert_rr is None:
        return False, "Sertraline refill request not found"
    if sert_rr.get("status") != "denied":
        return False, f"Sertraline refill status is '{sert_rr.get('status')}', expected 'denied'"
    reason = sert_rr.get("denyReason", "").lower()
    if "taper" not in reason:
        return False, f"Sertraline denial reason should mention tapering, got: '{sert_rr.get('denyReason')}'"

    return True, "Gabapentin approved (refills=5); Omeprazole approved (BID sig); Sertraline denied (tapering)"
