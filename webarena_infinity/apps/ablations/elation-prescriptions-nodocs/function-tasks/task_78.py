import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("settings", {})

    if settings.get("defaultPharmacy") != "pharm_009":
        return False, f"Default pharmacy should be 'pharm_009' (Capsule), got '{settings.get('defaultPharmacy')}'."

    return True, "Default pharmacy changed to Capsule Pharmacy SF (pharm_009)."
