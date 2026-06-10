import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    default_pharmacy = settings.get("defaultPharmacy", "")

    if default_pharmacy != "pharm_002":
        return False, f"Expected settings.defaultPharmacy to be 'pharm_002' (Walgreens #7893), but got '{default_pharmacy}'."

    return True, "Default pharmacy switched to Walgreens #7893 (pharm_002)."
