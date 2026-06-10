import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Main Office location name updated to 'SF Main Office'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    locations = state.get("practiceSettings", {}).get("practiceLocations", [])

    found_sf_main = False
    for loc in locations:
        if loc.get("name") == "Main Office":
            return False, "Location with name 'Main Office' still exists, expected it to be renamed to 'SF Main Office'"
        if loc.get("name") == "SF Main Office":
            found_sf_main = True

    if not found_sf_main:
        return False, "Location 'SF Main Office' not found in practiceLocations"

    return True, "Main Office location correctly renamed to 'SF Main Office'"
