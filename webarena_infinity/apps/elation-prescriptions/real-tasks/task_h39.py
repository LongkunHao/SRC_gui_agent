import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check default pharmacy changed to Express Scripts Mail Pharmacy
    settings = state.get("settings", {})
    default_pharm = settings.get("defaultPharmacyId")
    if default_pharm != "pharm_011":
        return False, f"Default pharmacy is '{default_pharm}', expected 'pharm_011' (Express Scripts Mail Pharmacy)"

    # Check Magnesium Citrate 400mg documented as OTC
    otc_meds = state.get("permanentOtcMeds", [])
    magnesium = None
    for med in otc_meds:
        name = med.get("medicationName", "").lower()
        if "magnesium" in name:
            magnesium = med
            break
    if magnesium is None:
        return False, "No Magnesium supplement found in permanentOtcMeds"

    if magnesium.get("classification") != "permanent_otc":
        return False, f"Magnesium classification is '{magnesium.get('classification')}', expected 'permanent_otc'"

    return True, "Default pharmacy set to Express Scripts, Magnesium Citrate documented as OTC"
