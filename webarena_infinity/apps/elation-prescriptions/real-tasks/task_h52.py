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
    change_requests = state.get("changeRequests", [])

    # Gabapentin refill should be approved with modifications
    gab_refill = None
    for r in refill_requests:
        if r.get("medicationName") == "Gabapentin 300mg capsule":
            gab_refill = r
            break
    if gab_refill is None:
        return False, "Gabapentin refill request not found"
    if gab_refill.get("status") != "approved":
        return False, f"Gabapentin refill status is '{gab_refill.get('status')}', expected 'approved'"

    # Check sig was modified to BID
    mods = gab_refill.get("modifications", {})
    mod_sig = mods.get("sig", "") if mods else ""
    if "twice daily" not in mod_sig.lower() and "bid" not in mod_sig.lower():
        # Check the actual med
        permanent_rx = state.get("permanentRxMeds", [])
        gab_med = None
        for m in permanent_rx:
            if m.get("medicationName") == "Gabapentin 300mg capsule":
                gab_med = m
                break
        if gab_med is None:
            return False, "Gabapentin not found in permanentRxMeds"
        if "twice daily" not in gab_med.get("sig", "").lower():
            return False, f"Gabapentin sig should be BID, got: '{gab_med.get('sig')}'"

    # Check refills set to 5
    mod_refills = mods.get("refills") if mods else None
    if mod_refills != 5:
        permanent_rx = state.get("permanentRxMeds", [])
        gab_med = None
        for m in permanent_rx:
            if m.get("medicationName") == "Gabapentin 300mg capsule":
                gab_med = m
                break
        if gab_med:
            ref = gab_med.get("refillsRemaining", gab_med.get("refills"))
            if ref != 5:
                return False, f"Gabapentin refills is {ref}, expected 5"

    # Gabapentin change request (dosing clarification) should be approved
    gab_cr = None
    for cr in change_requests:
        if cr.get("medicationName") == "Gabapentin 300mg capsule":
            gab_cr = cr
            break
    if gab_cr is None:
        return False, "Gabapentin change request not found"
    if gab_cr.get("status") != "approved":
        return False, f"Gabapentin change request status is '{gab_cr.get('status')}', expected 'approved'"

    return True, "Gabapentin refill approved (BID sig, 5 refills) and dosing clarification change request approved"
