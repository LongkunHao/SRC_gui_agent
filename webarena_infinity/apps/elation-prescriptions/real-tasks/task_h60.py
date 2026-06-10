import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    # The UTI temporary medication is Ciprofloxacin 500mg at Rite Aid #3456 (pharm_005)
    settings = state.get("settings", {})

    # Default pharmacy should be Rite Aid
    if settings.get("defaultPharmacyId") != "pharm_005":
        return False, (
            f"Default pharmacy is '{settings.get('defaultPharmacyId')}', "
            f"expected 'pharm_005' (Rite Aid #3456 — Ciprofloxacin's pharmacy)"
        )

    # Auto-populate should be disabled
    if settings.get("autoPopulateLastPharmacy") is not False:
        return False, "Auto-populate last used pharmacy should be disabled"

    # Formulary info should be disabled
    if settings.get("showFormularyData") is not False:
        return False, "Show formulary information should be disabled"

    return True, "Default pharmacy set to Rite Aid, auto-populate disabled, formulary display disabled"
