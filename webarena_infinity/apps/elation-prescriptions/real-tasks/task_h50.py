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

    # Cholesterol med = Atorvastatin 20mg tablet
    atorvastatin_req = None
    for r in refill_requests:
        if r.get("medicationName") == "Atorvastatin 20mg tablet":
            atorvastatin_req = r
            break
    if atorvastatin_req is None:
        return False, "Atorvastatin refill request not found"
    if atorvastatin_req.get("status") != "denied":
        return False, f"Atorvastatin refill status is '{atorvastatin_req.get('status')}', expected 'denied'"
    reason = atorvastatin_req.get("denyReason", "").lower()
    if "lipid" not in reason:
        return False, f"Atorvastatin denial should mention lipid panel, got: '{atorvastatin_req.get('denyReason')}'"

    # Lisinopril refill should also be denied
    lisinopril_req = None
    for r in refill_requests:
        if r.get("medicationName") == "Lisinopril 10mg tablet":
            lisinopril_req = r
            break
    if lisinopril_req is None:
        return False, "Lisinopril refill request not found"
    if lisinopril_req.get("status") != "denied":
        return False, f"Lisinopril refill status is '{lisinopril_req.get('status')}', expected 'denied'"
    reason = lisinopril_req.get("denyReason", "").lower()
    if "follow" not in reason and "blood pressure" not in reason and "appointment" not in reason:
        return False, f"Lisinopril denial should mention follow-up/BP check, got: '{lisinopril_req.get('denyReason')}'"

    return True, "Atorvastatin denied (lipid panel overdue), Lisinopril denied (BP follow-up needed)"
