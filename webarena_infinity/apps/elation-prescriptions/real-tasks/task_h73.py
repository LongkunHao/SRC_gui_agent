import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    rx_templates = state.get("rxTemplates", [])
    custom_sigs = state.get("customSigs", [])
    refill_requests = state.get("refillRequests", [])

    # Gabapentin template should exist
    gaba_tpl = None
    for tpl in rx_templates:
        if tpl.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_tpl = tpl
            break

    if gaba_tpl is None:
        return False, "Gabapentin 300mg capsule Rx template not found"

    sig = gaba_tpl.get("sig", "").lower()
    if "three times" not in sig and "tid" not in sig and "3 times" not in sig:
        return False, f"Gabapentin template sig should be TID, got: '{gaba_tpl.get('sig')}'"
    if gaba_tpl.get("qty") != 90:
        return False, f"Gabapentin template qty is {gaba_tpl.get('qty')}, expected 90"
    if gaba_tpl.get("refills") != 0:
        return False, f"Gabapentin template refills is {gaba_tpl.get('refills')}, expected 0"
    if gaba_tpl.get("daysSupply") != 30:
        return False, f"Gabapentin template daysSupply is {gaba_tpl.get('daysSupply')}, expected 30"

    # Custom PRN sig should exist
    prn_sig = None
    for s in custom_sigs:
        text = s.get("text", "").lower()
        if "bedtime" in text and "pain" in text and "needed" in text:
            prn_sig = s
            break

    if prn_sig is None:
        return False, "Custom PRN sig for bedtime pain not found"
    if prn_sig.get("category") != "prn":
        return False, f"Custom sig category is '{prn_sig.get('category')}', expected 'prn'"

    # Gabapentin refill request should be approved
    gaba_rr = None
    for r in refill_requests:
        if r.get("medicationName") == "Gabapentin 300mg capsule":
            gaba_rr = r
            break
    if gaba_rr is None:
        return False, "Gabapentin refill request not found"
    if gaba_rr.get("status") != "approved":
        return False, f"Gabapentin refill status is '{gaba_rr.get('status')}', expected 'approved'"

    return True, "Gabapentin template created; PRN sig added; Gabapentin refill approved"
