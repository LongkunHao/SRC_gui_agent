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
    settings = state.get("settings", {})

    # Atorvastatin refill should be denied
    atorva_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Atorvastatin 20mg tablet":
            atorva_rr = r
            break
    if atorva_rr is None:
        return False, "Atorvastatin refill request not found"
    if atorva_rr.get("status") != "denied":
        return False, f"Atorvastatin refill status is '{atorva_rr.get('status')}', expected 'denied'"

    # New Atorvastatin prescription at Express Scripts
    atorva_new = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "atorvastatin" in name and "20mg" in name:
            if med.get("pharmacyId") == "pharm_011":
                atorva_new = med
                break

    if atorva_new is None:
        return False, "No Atorvastatin 20mg prescription found at Express Scripts Mail Pharmacy"

    if atorva_new.get("qty") != 90:
        return False, f"Atorvastatin qty is {atorva_new.get('qty')}, expected 90"
    if atorva_new.get("refills") != 5:
        return False, f"Atorvastatin refills is {atorva_new.get('refills')}, expected 5"
    if atorva_new.get("daysSupply") != 90:
        return False, f"Atorvastatin daysSupply is {atorva_new.get('daysSupply')}, expected 90"

    # Default pharmacy should be Express Scripts
    if settings.get("defaultPharmacyId") != "pharm_011":
        return False, f"Default pharmacy is '{settings.get('defaultPharmacyId')}', expected 'pharm_011' (Express Scripts)"

    return True, "Atorvastatin refill denied, new Rx at Express Scripts, default pharmacy updated"
