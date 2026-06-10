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

    # CVS refills (pharm_001): Lisinopril, Atorvastatin, Gabapentin, Omeprazole, Metoprolol
    # Non-CVS refills (pharm_003 Walgreens): Sertraline
    cvs_meds = ["Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
                 "Gabapentin 300mg capsule", "Omeprazole 20mg capsule",
                 "Metoprolol Succinate ER 50mg tablet"]
    non_cvs_meds = ["Sertraline 50mg tablet"]

    for med_name in cvs_meds:
        req = None
        for r in refill_requests:
            if r.get("medicationName") == med_name:
                req = r
                break
        if req is None:
            return False, f"Refill request for {med_name} not found"
        if req.get("status") != "approved":
            return False, f"Refill for {med_name} should be approved (CVS), got '{req.get('status')}'"

    for med_name in non_cvs_meds:
        req = None
        for r in refill_requests:
            if r.get("medicationName") == med_name:
                req = r
                break
        if req is None:
            return False, f"Refill request for {med_name} not found"
        if req.get("status") != "denied":
            return False, f"Refill for {med_name} should be denied (non-CVS), got '{req.get('status')}'"
        reason = req.get("denyReason", "")
        if "cvs" not in reason.lower() and "transfer" not in reason.lower():
            return False, f"Deny reason for {med_name} should mention CVS/transfer, got: '{reason}'"

    return True, "CVS refills approved, non-CVS refills denied with transfer reason"
