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

    # ACE inhibitor = Lisinopril 10mg (CVS), ARB = Losartan 50mg (Walgreens)
    for med_name in ["Lisinopril 10mg tablet", "Losartan 50mg tablet"]:
        still_active = any(m.get("medicationName") == med_name for m in permanent_rx)
        if still_active:
            return False, f"{med_name} still in permanentRxMeds, should be discontinued"
        in_disc = any(m.get("medicationName") == med_name for m in discontinued)
        if not in_disc:
            return False, f"{med_name} not found in discontinuedMeds"
        in_canceled = any(c.get("medicationName") == med_name for c in canceled)
        if not in_canceled:
            return False, f"Cancellation for {med_name} not sent to pharmacy"

    # New Amlodipine 10mg should exist at CVS
    amlodipine_10 = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "amlodipine" in name.lower() and "10mg" in name.lower():
            amlodipine_10 = med
            break
    if amlodipine_10 is None:
        return False, "Amlodipine 10mg tablet not found in permanentRxMeds"

    if amlodipine_10.get("pharmacyId") != "pharm_001":
        return False, f"Amlodipine 10mg pharmacy is '{amlodipine_10.get('pharmacyName')}', expected CVS #4521"

    if amlodipine_10.get("qty") != 30:
        return False, f"Amlodipine 10mg qty is {amlodipine_10.get('qty')}, expected 30"

    refills = amlodipine_10.get("refills", amlodipine_10.get("refillsRemaining"))
    if refills != 3:
        return False, f"Amlodipine 10mg refills is {refills}, expected 3"

    if amlodipine_10.get("daysSupply") != 30:
        return False, f"Amlodipine 10mg daysSupply is {amlodipine_10.get('daysSupply')}, expected 30"

    return True, "Lisinopril and Losartan discontinued with cancellations, Amlodipine 10mg prescribed at CVS"
