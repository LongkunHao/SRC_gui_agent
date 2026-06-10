import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    old = next((c for c in state["contacts"] if c["name"] == "Meridian Health Clinic"), None)
    if old:
        return False, "Contact still named 'Meridian Health Clinic' — name was not updated."
    new = next((c for c in state["contacts"] if c["name"] == "Meridian Health & Wellness Clinic"), None)
    if not new:
        return False, "Contact 'Meridian Health & Wellness Clinic' not found."
    if new["id"] != "con_22":
        return False, f"Expected contact id 'con_22', got '{new['id']}'"
    return True, "Contact renamed to 'Meridian Health & Wellness Clinic' correctly."
