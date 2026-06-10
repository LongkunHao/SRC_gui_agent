import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultPharmacy") != "pharm_006":
        return False, f"Default pharmacy should be 'pharm_006' (Costco), got '{settings.get('defaultPharmacy')}'."

    return True, "Default pharmacy changed to Costco Pharmacy #482 (pharm_006)."
