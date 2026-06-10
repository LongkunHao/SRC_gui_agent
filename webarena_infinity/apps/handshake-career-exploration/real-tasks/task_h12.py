import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    locations = state.get("currentUser", {}).get("careerInterests", {}).get("locations", [])

    required = {"Boston, MA", "Chicago, IL", "Washington, DC"}
    old_locations = {"San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Remote"}

    errors = []

    # Check that all required locations are present
    for loc in required:
        if loc not in locations:
            errors.append(f"'{loc}' not found in locations.")

    # Check that none of the old locations remain
    for loc in old_locations:
        if loc in locations:
            errors.append(f"Old location '{loc}' still present in locations.")

    # Check that there are exactly 3 locations
    if len(locations) != len(required):
        errors.append(
            f"Expected exactly {len(required)} locations, found {len(locations)}: {locations}"
        )

    if errors:
        return False, f"Location check failed. Current locations: {locations}. Issues: {' | '.join(errors)}"

    return True, (
        f"Locations correctly updated to {locations}. "
        f"All old locations removed and new locations added."
    )
