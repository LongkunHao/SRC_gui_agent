import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultPharmacy") != "pharm_008":
        return False, f"Expected settings.defaultPharmacy 'pharm_008' (Express Scripts Mail Pharmacy), got '{settings.get('defaultPharmacy')}'."

    if settings.get("defaultDaysSupply") != 90:
        return False, f"Expected settings.defaultDaysSupply 90, got {settings.get('defaultDaysSupply')}."

    return True, "Default pharmacy set to Express Scripts Mail Pharmacy and default days supply set to 90."
