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

    # Most recently submitted: Metoprolol ER (2026-03-01T09:30:00Z) — should be approved
    metoprolol_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Metoprolol Succinate ER 50mg tablet":
            metoprolol_rr = r
            break
    if metoprolol_rr is None:
        return False, "Metoprolol refill request not found"
    if metoprolol_rr.get("status") != "approved":
        return False, f"Metoprolol refill status is '{metoprolol_rr.get('status')}', expected 'approved'"

    # All other pending refills should be denied
    other_meds = [
        "Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
        "Gabapentin 300mg capsule", "Omeprazole 20mg capsule",
        "Sertraline 50mg tablet"
    ]
    for med_name in other_meds:
        rr = None
        for r in refill_requests:
            if r.get("medicationName") == med_name:
                rr = r
                break
        if rr is None:
            continue  # already processed or not found
        if rr.get("status") != "denied":
            return False, f"Refill for {med_name} status is '{rr.get('status')}', expected 'denied'"
        reason = rr.get("denyReason", "").lower()
        if "batch" not in reason and "resubmit" not in reason:
            return False, f"Denial reason for {med_name} should mention batch/resubmit, got: '{rr.get('denyReason')}'"

    return True, "Most recent refill (Metoprolol) approved; all others denied for batch resubmission"
