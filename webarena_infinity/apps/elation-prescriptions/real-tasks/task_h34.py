import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Sertraline (anxiety med at Walgreens) — refill should be approved
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

    # Losartan (BP med at Walgreens, prescribed by Dr. Chen) — should be discontinued
    permanent_rx = state.get("permanentRxMeds", [])
    discontinued = state.get("discontinuedMeds", [])

    for med in permanent_rx:
        if med.get("medicationName") == "Losartan 50mg tablet":
            return False, "Losartan 50mg tablet still in permanentRxMeds, should be discontinued"

    losartan_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Losartan 50mg tablet":
            losartan_disc = med
            break
    if losartan_disc is None:
        return False, "Losartan 50mg tablet not found in discontinuedMeds"

    # Sertraline should still be active
    sertraline_active = None
    for med in permanent_rx:
        if med.get("medicationName") == "Sertraline 50mg tablet":
            sertraline_active = med
            break
    if sertraline_active is None:
        return False, "Sertraline 50mg tablet missing from permanentRxMeds"

    return True, "Sertraline refill approved, Losartan discontinued (different provider)"
