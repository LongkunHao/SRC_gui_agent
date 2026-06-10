import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    change_requests = state.get("changeRequests", [])

    # cr_001: Atorvastatin therapeutic substitution → approve
    atorvastatin_cr = None
    for cr in change_requests:
        if cr.get("originalMedication") == "Atorvastatin 20mg tablet":
            atorvastatin_cr = cr
            break
    if atorvastatin_cr is None:
        return False, "Atorvastatin change request not found"
    if atorvastatin_cr.get("status") != "approved":
        return False, f"Atorvastatin substitution status is '{atorvastatin_cr.get('status')}', expected 'approved'"

    # cr_002: Gabapentin dosing clarification → deny
    gabapentin_cr = None
    for cr in change_requests:
        if cr.get("medicationName") == "Gabapentin 300mg capsule":
            gabapentin_cr = cr
            break
    if gabapentin_cr is None:
        return False, "Gabapentin change request not found"
    if gabapentin_cr.get("status") != "denied":
        return False, f"Gabapentin clarification status is '{gabapentin_cr.get('status')}', expected 'denied'"
    reason = gabapentin_cr.get("denyReason", "").lower()
    if "tid" not in reason and "three times" not in reason and "correct" not in reason:
        return False, f"Denial reason should mention TID/correct dosing, got: '{gabapentin_cr.get('denyReason')}'"

    return True, "Atorvastatin substitution approved, Gabapentin clarification denied with TID confirmation"
