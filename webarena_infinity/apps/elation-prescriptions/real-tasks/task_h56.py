import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The temporary antibiotic prescribed by urgent care (not current provider):
    # Ciprofloxacin 500mg tablet, prescribed by Dr. Lisa Park (prov_003, Urgent Care)
    # at Rite Aid #3456
    temporary = state.get("temporaryMeds", [])
    permanent_rx = state.get("permanentRxMeds", [])

    # Ciprofloxacin should be moved to permanent Rx
    cipro_temp = any(m.get("medicationName") == "Ciprofloxacin 500mg tablet" for m in temporary)
    if cipro_temp:
        return False, "Ciprofloxacin still in temporaryMeds, should be moved to permanent Rx"

    cipro_perm = None
    for m in permanent_rx:
        if m.get("medicationName") == "Ciprofloxacin 500mg tablet":
            cipro_perm = m
            break
    if cipro_perm is None:
        return False, "Ciprofloxacin not found in permanentRxMeds"
    if cipro_perm.get("classification") != "permanent_rx":
        return False, f"Ciprofloxacin classification is '{cipro_perm.get('classification')}', expected 'permanent_rx'"

    # Ciprofloxacin's pharmacy is Rite Aid (pharm_005).
    # There's no change request from Rite Aid — change requests are from CVS (pharm_001).
    # The Atorvastatin substitution (cr_001) is from CVS — therapeutic substitution → doesn't apply
    # The Gabapentin clarification (cr_002) is from CVS — dosing clarification → deny it
    change_requests = state.get("changeRequests", [])
    gab_cr = None
    for cr in change_requests:
        if cr.get("medicationName") == "Gabapentin 300mg capsule":
            gab_cr = cr
            break
    if gab_cr is None:
        return False, "Gabapentin change request not found"
    if gab_cr.get("status") != "denied":
        return False, f"Gabapentin dosing clarification should be denied, got '{gab_cr.get('status')}'"

    return True, "Ciprofloxacin moved to permanent Rx, Gabapentin dosing clarification denied"
