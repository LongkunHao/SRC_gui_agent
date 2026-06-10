import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The only non-controlled med with 0 refills remaining is Gabapentin 300mg
    # (refillsRemaining: 0, isControlled: false)
    # Alprazolam also has 0 refills but IS controlled (Schedule IV)
    refill_requests = state.get("refillRequests", [])

    gabapentin_req = None
    for r in refill_requests:
        if r.get("medicationName") == "Gabapentin 300mg capsule":
            gabapentin_req = r
            break

    if gabapentin_req is None:
        return False, "Gabapentin 300mg capsule refill request not found"

    if gabapentin_req.get("status") != "approved":
        return False, f"Gabapentin refill status is '{gabapentin_req.get('status')}', expected 'approved'"

    # Check refills were increased to 3
    mods = gabapentin_req.get("modifications", {})
    if not mods or mods.get("refills") != 3:
        # Also check the med itself
        permanent_rx = state.get("permanentRxMeds", [])
        gabapentin_med = None
        for m in permanent_rx:
            if m.get("medicationName") == "Gabapentin 300mg capsule":
                gabapentin_med = m
                break
        if gabapentin_med is None:
            return False, "Gabapentin 300mg capsule not found in permanentRxMeds"
        refills = gabapentin_med.get("refillsRemaining", gabapentin_med.get("refills"))
        if refills != 3:
            return False, f"Gabapentin refills is {refills}, expected 3"

    return True, "Gabapentin refill approved with refills increased to 3"
