import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # Check Sulfonamides allergy removed
    allergies = state.get("currentPatient", {}).get("allergies", [])
    for allergy in allergies:
        if "sulfonamide" in allergy.get("allergen", "").lower():
            return False, "Sulfonamides allergy still present in patient allergies"

    # Check TMP-SMX prescribed as temporary
    temporary = state.get("temporaryMeds", [])
    tmp_smx = None
    for med in temporary:
        name = med.get("medicationName", "").lower()
        if "trimethoprim" in name or "sulfamethoxazole" in name:
            tmp_smx = med
            break
    if tmp_smx is None:
        # Check permanentRxMeds as fallback
        for med in state.get("permanentRxMeds", []):
            name = med.get("medicationName", "").lower()
            if "trimethoprim" in name or "sulfamethoxazole" in name:
                return False, "TMP-SMX found in permanentRxMeds but should be temporary"
        return False, "No Trimethoprim-Sulfamethoxazole found in temporaryMeds"

    qty = tmp_smx.get("qty")
    if qty != 14:
        return False, f"TMP-SMX qty is {qty}, expected 14"

    refills = tmp_smx.get("refills", tmp_smx.get("refillsRemaining"))
    if refills != 0:
        return False, f"TMP-SMX refills is {refills}, expected 0"

    days = tmp_smx.get("daysSupply")
    if days != 7:
        return False, f"TMP-SMX daysSupply is {days}, expected 7"

    pharmacy_id = tmp_smx.get("pharmacyId", "")
    pharmacy_name = tmp_smx.get("pharmacyName", "")
    if pharmacy_id != "pharm_001" and "cvs" not in pharmacy_name.lower():
        return False, f"TMP-SMX pharmacy is '{pharmacy_name}' ({pharmacy_id}), expected CVS #4521"

    return True, "Sulfonamides allergy removed, TMP-SMX 800mg/160mg prescribed as temporary to CVS"
