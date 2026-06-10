import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultPharmacy") != "pharm_010":
        return False, f"Default pharmacy should be 'pharm_010' (BioPlus), got '{settings.get('defaultPharmacy')}'."

    if settings.get("defaultDaysSupply") != 60:
        return False, f"Default days supply should be 60, got {settings.get('defaultDaysSupply')}."

    return True, "Default pharmacy changed to BioPlus (pharm_010) and default days supply changed to 60."
