import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The beta-blocker is Metoprolol Succinate ER 50mg
    refill_requests = state.get("refillRequests", [])
    metoprolol_refill = None
    for req in refill_requests:
        if req.get("medicationName") == "Metoprolol Succinate ER 50mg tablet" or req.get("id") == "rr_008":
            metoprolol_refill = req
            break
    if metoprolol_refill is None:
        return False, "Metoprolol refill request not found"
    if metoprolol_refill.get("status") != "approved":
        return False, f"Metoprolol refill status is '{metoprolol_refill.get('status')}', expected 'approved'"

    # Check modifications include sig change
    mods = metoprolol_refill.get("modifications", {})
    if not mods or "sig" not in mods:
        return False, "Metoprolol refill was approved but without sig modification"

    mod_sig = mods.get("sig", "").lower()
    if "morning" not in mod_sig:
        return False, f"Metoprolol modified sig is '{mods.get('sig')}', expected sig mentioning 'morning'"

    # Also check the medication's sig was updated
    permanent_rx = state.get("permanentRxMeds", [])
    metoprolol_med = None
    for med in permanent_rx:
        if med.get("medicationName") == "Metoprolol Succinate ER 50mg tablet":
            metoprolol_med = med
            break
    if metoprolol_med is not None:
        med_sig = metoprolol_med.get("sig", "").lower()
        if "morning" not in med_sig:
            return False, f"Metoprolol medication sig not updated to morning dosing: '{metoprolol_med.get('sig')}'"

    return True, "Metoprolol (beta-blocker) refill approved with sig modified to morning dosing"
