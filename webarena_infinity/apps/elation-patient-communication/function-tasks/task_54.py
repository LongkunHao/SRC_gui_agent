import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify 'East Bay Clinic' practice location removed."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    locations = state.get("practiceSettings", {}).get("practiceLocations", [])

    for loc in locations:
        if loc.get("name") == "East Bay Clinic":
            return False, "Practice location 'East Bay Clinic' still exists, expected it to be removed"

    if len(locations) != 2:
        return False, f"Expected 2 practice locations after removal, found {len(locations)}"

    return True, "Practice location 'East Bay Clinic' correctly removed (2 locations remain)"
