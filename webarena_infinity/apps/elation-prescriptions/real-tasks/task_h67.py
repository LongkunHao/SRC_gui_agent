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

    # Losartan (ARB, started 2025-06-15) should be discontinued
    losartan_active = any(
        m.get("medicationName") == "Losartan 50mg tablet" for m in permanent_rx
    )
    if losartan_active:
        return False, "Losartan 50mg tablet still active — should be discontinued (ARB in interaction)"

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

    # Lisinopril 10mg should still be active (started earlier, keep)
    lisinopril_10_active = any(
        m.get("medicationName") == "Lisinopril 10mg tablet" for m in permanent_rx
    )
    if not lisinopril_10_active:
        return False, "Lisinopril 10mg tablet was removed but should remain"

    # Lisinopril 20mg should be prescribed as step-up dose
    lisinopril_20 = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "lisinopril" in name and "20mg" in name:
            lisinopril_20 = med
            break

    if lisinopril_20 is None:
        return False, "Lisinopril 20mg not found in permanentRxMeds (step-up dose)"

    if lisinopril_20.get("pharmacyId") != "pharm_001":
        return False, f"Lisinopril 20mg pharmacy is '{lisinopril_20.get('pharmacyName')}', expected CVS #4521"
    if lisinopril_20.get("qty") != 30:
        return False, f"Lisinopril 20mg qty is {lisinopril_20.get('qty')}, expected 30"
    if lisinopril_20.get("refills") != 3:
        return False, f"Lisinopril 20mg refills is {lisinopril_20.get('refills')}, expected 3"
    if lisinopril_20.get("daysSupply") != 30:
        return False, f"Lisinopril 20mg daysSupply is {lisinopril_20.get('daysSupply')}, expected 30"

    return True, "Losartan (ARB) discontinued with cancellation; Lisinopril stepped up to 20mg at CVS"
