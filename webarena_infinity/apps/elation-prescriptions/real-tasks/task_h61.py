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

    # All 6 pending refills should now be approved
    pending_meds = [
        "Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
        "Gabapentin 300mg capsule", "Omeprazole 20mg capsule",
        "Sertraline 50mg tablet", "Metoprolol Succinate ER 50mg tablet"
    ]

    for med_name in pending_meds:
        rr = None
        for r in refill_requests:
            if r.get("medicationName") == med_name:
                rr = r
                break
        if rr is None:
            return False, f"Refill request for {med_name} not found"
        if rr.get("status") != "approved":
            return False, f"Refill for {med_name} status is '{rr.get('status')}', expected 'approved'"

    # Gabapentin had 0 refills remaining — should be approved with refills=3
    gaba_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_rr = r
            break
    mods = gaba_rr.get("modifications", {})
    if mods.get("refills") != 3:
        return False, f"Gabapentin should have modifications.refills=3, got {mods}"

    gaba_med = None
    for m in permanent_rx:
        if m.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_med = m
            break
    if gaba_med and gaba_med.get("refillsRemaining") != 3:
        return False, f"Gabapentin refillsRemaining is {gaba_med.get('refillsRemaining')}, expected 3"

    return True, "All pending refills approved; Gabapentin approved with refills increased to 3"
