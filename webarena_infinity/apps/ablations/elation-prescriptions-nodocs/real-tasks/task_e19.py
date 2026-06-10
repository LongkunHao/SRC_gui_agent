import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    settings = state.get("settings", {})
    default_days_supply = settings.get("defaultDaysSupply")

    if default_days_supply != 90:
        return False, f"Expected settings.defaultDaysSupply to be 90, but got {default_days_supply}."

    return True, "Default days supply set to 90."
