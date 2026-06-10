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

    # Check original Metformin 500mg at CVS is discontinued
    metformin_disc = None
    for med in discontinued:
        if med.get("medicationName") == "Metformin 500mg tablet":
            metformin_disc = med
            break
    if metformin_disc is None:
        return False, "Original Metformin 500mg tablet not found in discontinuedMeds"

    # Check new Metformin 500mg at Express Scripts exists
    metformin_new = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "metformin" in name and "500mg" in name:
            metformin_new = med
            break
    if metformin_new is None:
        return False, "No new Metformin 500mg found in permanentRxMeds"

    # Check pharmacy is Express Scripts
    pharmacy_id = metformin_new.get("pharmacyId", "")
    pharmacy_name = metformin_new.get("pharmacyName", "")
    if pharmacy_id != "pharm_011" and "express scripts" not in pharmacy_name.lower():
        return False, f"New Metformin pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected Express Scripts Mail Pharmacy"

    qty = metformin_new.get("qty")
    if qty != 180:
        return False, f"New Metformin qty is {qty}, expected 180"

    refills = metformin_new.get("refills", metformin_new.get("refillsRemaining"))
    if refills != 5:
        return False, f"New Metformin refills is {refills}, expected 5"

    days = metformin_new.get("daysSupply")
    if days != 90:
        return False, f"New Metformin daysSupply is {days}, expected 90"

    return True, "Metformin transferred: original at CVS discontinued, new at Express Scripts (qty 180, 5 refills, 90 days)"
