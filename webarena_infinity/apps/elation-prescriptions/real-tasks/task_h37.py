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

    # Gabapentin (rr_003) has notes — should be approved
    gabapentin_refill = None
    for req in refill_requests:
        if req.get("medicationName") == "Gabapentin 300mg capsule" or req.get("id") == "rr_003":
            gabapentin_refill = req
            break
    if gabapentin_refill is None:
        return False, "Gabapentin refill request not found"
    if gabapentin_refill.get("status") != "approved":
        return False, f"Gabapentin refill status is '{gabapentin_refill.get('status')}', expected 'approved' (has pharmacy notes)"

    # All other pending refills have no notes — should be denied
    no_note_refills = {
        "rr_001": "Lisinopril 10mg tablet",
        "rr_002": "Atorvastatin 20mg tablet",
        "rr_004": "Omeprazole 20mg capsule",
        "rr_007": "Sertraline 50mg tablet",
        "rr_008": "Metoprolol Succinate ER 50mg tablet",
    }

    for rr_id, med_name in no_note_refills.items():
        req = None
        for r in refill_requests:
            if r.get("id") == rr_id or r.get("medicationName") == med_name:
                req = r
                break
        if req is None:
            return False, f"Refill request for {med_name} ({rr_id}) not found"
        if req.get("status") != "denied":
            return False, f"Refill for {med_name} status is '{req.get('status')}', expected 'denied' (no pharmacy notes)"

    # Check no pending refills remain
    pending = sum(1 for r in refill_requests if r.get("status") == "pending")
    if pending > 0:
        return False, f"Still have {pending} pending refill request(s), expected 0"

    return True, "Gabapentin refill approved (has notes), 5 other refills denied (no notes)"
