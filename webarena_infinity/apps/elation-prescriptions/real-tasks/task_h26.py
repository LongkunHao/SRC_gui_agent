import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Atorvastatin refill is approved
    refill_requests = state.get("refillRequests", [])
    atorvastatin_refill = None
    for req in refill_requests:
        if req.get("medicationName") == "Atorvastatin 20mg tablet" or req.get("id") == "rr_002":
            atorvastatin_refill = req
            break
    if atorvastatin_refill is None:
        return False, "Atorvastatin refill request not found"
    if atorvastatin_refill.get("status") != "approved":
        return False, f"Atorvastatin refill status is '{atorvastatin_refill.get('status')}', expected 'approved'"

    # Check Rosuvastatin 10mg Rx template exists
    templates = state.get("rxTemplates", [])
    rosuvastatin_tpl = None
    for tpl in templates:
        name = tpl.get("medicationName", "").lower()
        if "rosuvastatin" in name and "10mg" in name:
            rosuvastatin_tpl = tpl
            break
    if rosuvastatin_tpl is None:
        return False, "No Rosuvastatin 10mg Rx template found"

    if rosuvastatin_tpl.get("qty") != 30:
        return False, f"Rosuvastatin template qty is {rosuvastatin_tpl.get('qty')}, expected 30"

    if rosuvastatin_tpl.get("refills") != 5:
        return False, f"Rosuvastatin template refills is {rosuvastatin_tpl.get('refills')}, expected 5"

    if rosuvastatin_tpl.get("daysSupply") != 30:
        return False, f"Rosuvastatin template daysSupply is {rosuvastatin_tpl.get('daysSupply')}, expected 30"

    return True, "Atorvastatin refill approved and Rosuvastatin 10mg Rx template created"
