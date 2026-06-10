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

    # Check for new Lisinopril prescription at CVS with bulk params
    lisinopril_new = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "lisinopril" in name.lower() and "10mg" in name.lower():
            if med.get("qty") == 90 and med.get("daysSupply") == 90:
                lisinopril_new = med
                break
    if lisinopril_new is None:
        return False, "New Lisinopril 10mg with qty 90 / 90 days supply not found"

    if lisinopril_new.get("pharmacyId") != "pharm_001":
        return False, f"Lisinopril pharmacy is '{lisinopril_new.get('pharmacyName')}', expected CVS #4521"

    refills = lisinopril_new.get("refills", lisinopril_new.get("refillsRemaining"))
    if refills != 5:
        return False, f"Lisinopril refills is {refills}, expected 5"

    sig = lisinopril_new.get("sig", "")
    if "once daily" not in sig.lower():
        return False, f"Lisinopril sig doesn't match existing: '{sig}'"

    # Check for new Metformin prescription at CVS with bulk params
    metformin_new = None
    for med in permanent_rx:
        name = med.get("medicationName", "")
        if "metformin" in name.lower() and "500mg" in name.lower():
            if med.get("qty") == 90 and med.get("daysSupply") == 90:
                metformin_new = med
                break
    if metformin_new is None:
        return False, "New Metformin 500mg with qty 90 / 90 days supply not found"

    if metformin_new.get("pharmacyId") != "pharm_001":
        return False, f"Metformin pharmacy is '{metformin_new.get('pharmacyName')}', expected CVS #4521"

    refills = metformin_new.get("refills", metformin_new.get("refillsRemaining"))
    if refills != 5:
        return False, f"Metformin refills is {refills}, expected 5"

    sig = metformin_new.get("sig", "")
    if "twice daily" not in sig.lower():
        return False, f"Metformin sig doesn't match existing: '{sig}'"

    return True, "Lisinopril and Metformin bulk refills created at CVS (qty 90, 5 refills, 90 days)"
