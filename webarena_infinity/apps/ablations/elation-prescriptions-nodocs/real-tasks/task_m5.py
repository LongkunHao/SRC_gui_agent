import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultPharmacy") != "pharm_004":
        return False, f"Expected settings.defaultPharmacy 'pharm_004' (UCSF Medical Center Pharmacy), got '{settings.get('defaultPharmacy')}'."

    if settings.get("defaultRefills") != 3:
        return False, f"Expected settings.defaultRefills 3, got {settings.get('defaultRefills')}."

    return True, "Default pharmacy set to UCSF Medical Center Pharmacy and default refills increased to 3."
