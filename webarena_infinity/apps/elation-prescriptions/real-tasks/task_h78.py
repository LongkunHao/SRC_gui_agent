import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    settings = state.get("settings", {})
    dds = settings.get("drugDecisionSupport", {})
    rx_templates = state.get("rxTemplates", [])

    # Settings checks
    if settings.get("autoPopulateLastPharmacy") is not False:
        return False, "Auto-populate last used pharmacy should be disabled"

    if dds.get("drugToDrugLevel") != "major_only":
        return False, f"Drug interaction alerts is '{dds.get('drugToDrugLevel')}', expected 'major_only'"

    if settings.get("showCostEstimates") is not False:
        return False, "Show cost estimates should be disabled"

    # Amoxicillin template should be deleted
    amox_tpl = any(
        tpl.get("medicationName") == "Amoxicillin 500mg capsule" for tpl in rx_templates
    )
    if amox_tpl:
        return False, "Amoxicillin 500mg capsule template should be deleted"

    # Azithromycin Z-Pack template should be deleted
    azith_tpl = any(
        tpl.get("medicationName") == "Azithromycin 250mg tablet (Z-Pack)" for tpl in rx_templates
    )
    if azith_tpl:
        return False, "Azithromycin Z-Pack template should be deleted"

    return True, "Settings updated (auto-populate off, Major only, cost off); antibiotic templates deleted"
