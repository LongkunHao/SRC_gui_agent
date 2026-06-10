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
    permanent_otc = state.get("permanentOtcMeds", [])
    discontinued = state.get("discontinuedMeds", [])

    # Omeprazole (GERD med) should be discontinued
    omeprazole_active = any(
        m.get("medicationName") == "Omeprazole 20mg capsule" for m in permanent_rx
    )
    if omeprazole_active:
        return False, "Omeprazole 20mg capsule still active, should be discontinued"
    omeprazole_disc = any(
        m.get("medicationName") == "Omeprazole 20mg capsule" for m in discontinued
    )
    if not omeprazole_disc:
        return False, "Omeprazole 20mg capsule not found in discontinuedMeds"

    # Melatonin (bedtime sleep supplement) should be discontinued
    melatonin_active = any(
        m.get("medicationName") == "Melatonin 3mg tablet" for m in permanent_otc
    )
    if melatonin_active:
        return False, "Melatonin 3mg tablet still active, should be discontinued"
    melatonin_disc = any(
        m.get("medicationName") == "Melatonin 3mg tablet" for m in discontinued
    )
    if not melatonin_disc:
        return False, "Melatonin 3mg tablet not found in discontinuedMeds"

    # Famotidine 40mg should be prescribed
    famotidine = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "famotidine" in name.lower() and "40mg" in name.lower():
            famotidine = med
            break
    if famotidine is None:
        return False, "Famotidine 40mg tablet not found in permanentRxMeds"

    if famotidine.get("pharmacyId") != "pharm_001":
        return False, f"Famotidine pharmacy is '{famotidine.get('pharmacyName')}', expected CVS #4521"
    if famotidine.get("qty") != 30:
        return False, f"Famotidine qty is {famotidine.get('qty')}, expected 30"
    refills = famotidine.get("refills", famotidine.get("refillsRemaining"))
    if refills != 3:
        return False, f"Famotidine refills is {refills}, expected 3"
    if famotidine.get("daysSupply") != 30:
        return False, f"Famotidine daysSupply is {famotidine.get('daysSupply')}, expected 30"

    return True, "Omeprazole and Melatonin discontinued, Famotidine 40mg prescribed at CVS"
