import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check settings: drug interaction alerts = Major only
    settings = state.get("settings", {})
    dds = settings.get("drugDecisionSupport", {})
    level = dds.get("drugToDrugLevel")
    if level != "major_only":
        return False, f"Drug interaction alert level is '{level}', expected 'major_only'"

    # Check settings: cost estimates disabled
    if settings.get("showCostEstimates") is not False:
        return False, f"showCostEstimates is {settings.get('showCostEstimates')}, expected false"

    # Check Cyclobenzaprine 10mg prescribed
    permanent_rx = state.get("permanentRxMeds", [])
    cyclobenzaprine = None
    for med in permanent_rx:
        name = med.get("medicationName", "").lower()
        if "cyclobenzaprine" in name and "10mg" in name:
            cyclobenzaprine = med
            break
    if cyclobenzaprine is None:
        return False, "No Cyclobenzaprine 10mg found in permanentRxMeds"

    qty = cyclobenzaprine.get("qty")
    if qty != 30:
        return False, f"Cyclobenzaprine qty is {qty}, expected 30"

    refills = cyclobenzaprine.get("refills", cyclobenzaprine.get("refillsRemaining"))
    if refills != 1:
        return False, f"Cyclobenzaprine refills is {refills}, expected 1"

    pharmacy_id = cyclobenzaprine.get("pharmacyId", "")
    pharmacy_name = cyclobenzaprine.get("pharmacyName", "")
    if pharmacy_id != "pharm_001" and "cvs" not in pharmacy_name.lower():
        return False, f"Cyclobenzaprine pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected CVS #4521"

    return True, "Settings updated (Major only alerts, cost estimates off) and Cyclobenzaprine 10mg prescribed"
