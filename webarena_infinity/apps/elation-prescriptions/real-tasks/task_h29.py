import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The Walgreens refill is Sertraline (rr_007)
    refill_requests = state.get("refillRequests", [])
    sertraline_refill = None
    for req in refill_requests:
        if req.get("medicationName") == "Sertraline 50mg tablet" or req.get("id") == "rr_007":
            sertraline_refill = req
            break
    if sertraline_refill is None:
        return False, "Sertraline refill request not found"
    if sertraline_refill.get("status") != "approved":
        return False, f"Sertraline refill status is '{sertraline_refill.get('status')}', expected 'approved'"

    # Check refills modification to 11
    mods = sertraline_refill.get("modifications", {})
    if not mods:
        return False, "Sertraline refill approved but without modifications"
    mod_refills = mods.get("refills")
    if mod_refills != 11:
        return False, f"Sertraline refill modification refills is {mod_refills}, expected 11"

    # Check medication refillsRemaining updated
    permanent_rx = state.get("permanentRxMeds", [])
    sertraline_med = None
    for med in permanent_rx:
        if med.get("medicationName") == "Sertraline 50mg tablet":
            sertraline_med = med
            break
    if sertraline_med is not None:
        remaining = sertraline_med.get("refillsRemaining")
        if remaining != 11:
            return False, f"Sertraline refillsRemaining is {remaining}, expected 11"

    # Check default pharmacy changed to Walgreens
    settings = state.get("settings", {})
    default_pharm = settings.get("defaultPharmacyId")
    if default_pharm != "pharm_003":
        return False, f"Default pharmacy is '{default_pharm}', expected 'pharm_003' (Walgreens #7892)"

    return True, "Sertraline refill approved with 11 refills, default pharmacy set to Walgreens #7892"
