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

    # Losartan (Dr. Michael Chen, BP med) should be discontinued with cancellation
    losartan_active = any(
        m.get("medicationName") == "Losartan 50mg tablet" for m in permanent_rx
    )
    if losartan_active:
        return False, "Losartan 50mg tablet still active — should be discontinued (BP med by other provider)"

    losartan_disc = any(
        m.get("medicationName") == "Losartan 50mg tablet" for m in discontinued
    )
    if not losartan_disc:
        return False, "Losartan 50mg tablet not found in discontinuedMeds"

    losartan_canceled = any(
        c.get("medicationName") == "Losartan 50mg tablet" for c in canceled
    )
    if not losartan_canceled:
        return False, "Cancellation for Losartan not sent to pharmacy"

    # Ciprofloxacin (Dr. Lisa Park, non-BP med) should be in permanent Rx
    cipro_permanent = any(
        m.get("medicationName") == "Ciprofloxacin 500mg tablet" and
        m.get("classification") == "permanent_rx"
        for m in permanent_rx
    )
    if not cipro_permanent:
        return False, "Ciprofloxacin 500mg tablet should be in permanentRxMeds (moved from temporary)"

    # Ciprofloxacin should NOT be in temporary meds
    cipro_temp = any(
        m.get("medicationName") == "Ciprofloxacin 500mg tablet"
        for m in state.get("temporaryMeds", [])
    )
    if cipro_temp:
        return False, "Ciprofloxacin 500mg tablet still in temporaryMeds — should be moved to permanent"

    return True, "Losartan (BP, other provider) discontinued with cancellation; Ciprofloxacin moved to permanent"
