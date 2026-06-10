import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    permanent_rx = state.get("permanentRxMeds", [])
    discontinued = state.get("discontinuedMeds", [])
    canceled = state.get("canceledScripts", [])

    # Alprazolam (controlled anxiety med) should be discontinued
    alprazolam_active = any(
        m.get("medicationName") == "Alprazolam 0.5mg tablet" for m in permanent_rx
    )
    if alprazolam_active:
        return False, "Alprazolam 0.5mg tablet still active — should be discontinued"

    alprazolam_disc = any(
        m.get("medicationName") == "Alprazolam 0.5mg tablet" for m in discontinued
    )
    if not alprazolam_disc:
        return False, "Alprazolam 0.5mg tablet not found in discontinuedMeds"

    # Cancellation should be sent
    alprazolam_canceled = any(
        c.get("medicationName") == "Alprazolam 0.5mg tablet" for c in canceled
    )
    if not alprazolam_canceled:
        return False, "Cancellation for Alprazolam not sent to pharmacy"

    # Sertraline (non-controlled anxiety med) should still be active
    sertraline_active = any(
        m.get("medicationName") == "Sertraline 50mg tablet" for m in permanent_rx
    )
    if not sertraline_active:
        return False, "Sertraline 50mg tablet was removed but should remain (non-controlled)"

    # Buspirone should be prescribed at CVS (same pharmacy as Alprazolam)
    buspirone = None
    for med in permanent_rx:
        if "buspirone" in med.get("medicationName", "").lower():
            buspirone = med
            break
    if buspirone is None:
        return False, "Buspirone not found in permanentRxMeds"

    if buspirone.get("pharmacyId") != "pharm_001":
        return False, f"Buspirone pharmacy is '{buspirone.get('pharmacyName')}', expected CVS #4521"
    if buspirone.get("qty") != 60:
        return False, f"Buspirone qty is {buspirone.get('qty')}, expected 60"
    if buspirone.get("refills") != 5:
        return False, f"Buspirone refills is {buspirone.get('refills')}, expected 5"
    if buspirone.get("daysSupply") != 30:
        return False, f"Buspirone daysSupply is {buspirone.get('daysSupply')}, expected 30"

    return True, "Alprazolam discontinued with cancellation; Buspirone prescribed at same pharmacy"
