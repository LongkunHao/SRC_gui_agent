import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify new practice location 'South Bay Clinic' added with correct details."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    locations = state.get("practiceSettings", {}).get("practiceLocations", [])

    location = None
    for loc in locations:
        if loc.get("name") == "South Bay Clinic":
            location = loc
            break

    if location is None:
        return False, "Practice location 'South Bay Clinic' not found in practiceLocations"

    address = location.get("address")
    if address != "789 Stevens Creek Blvd, San Jose, CA 95128":
        return False, f"South Bay Clinic address is '{address}', expected '789 Stevens Creek Blvd, San Jose, CA 95128'"

    pos_code = location.get("posCode")
    if pos_code != "11":
        return False, f"South Bay Clinic posCode is '{pos_code}', expected '11'"

    pos_desc = location.get("posDescription")
    if pos_desc != "Office":
        return False, f"South Bay Clinic posDescription is '{pos_desc}', expected 'Office'"

    return True, "Practice location 'South Bay Clinic' correctly added with address, posCode, and posDescription"
