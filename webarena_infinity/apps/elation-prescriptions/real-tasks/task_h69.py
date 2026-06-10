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

    # Lisinopril has a major drug-drug interaction with Losartan — should be denied
    lisinopril_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Lisinopril 10mg tablet":
            lisinopril_rr = r
            break

    if lisinopril_rr is None:
        return False, "Lisinopril refill request not found"
    if lisinopril_rr.get("status") != "denied":
        return False, f"Lisinopril refill status is '{lisinopril_rr.get('status')}', expected 'denied' (drug interaction)"

    reason = lisinopril_rr.get("denyReason", "").lower()
    if "interaction" not in reason:
        return False, f"Lisinopril denial reason should mention drug interaction, got: '{lisinopril_rr.get('denyReason')}'"

    # All other pending refills should be approved
    approve_meds = [
        "Atorvastatin 20mg tablet", "Gabapentin 300mg capsule",
        "Omeprazole 20mg capsule", "Sertraline 50mg tablet",
        "Metoprolol Succinate ER 50mg tablet"
    ]
    for med_name in approve_meds:
        rr = None
        for r in refill_requests:
            if r.get("medicationName") == med_name:
                rr = r
                break
        if rr is None:
            continue
        if rr.get("status") != "approved":
            return False, f"Refill for {med_name} status is '{rr.get('status')}', expected 'approved'"

    return True, "Lisinopril refill denied (drug interaction); all others approved"
