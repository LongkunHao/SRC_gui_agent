import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    locations = (
        state.get("currentUser", {})
        .get("careerInterests", {})
        .get("locations", [])
    )

    has_boston = "Boston, MA" in locations
    has_denver = "Denver, CO" in locations

    if has_boston and has_denver:
        return True, f"Both 'Boston, MA' and 'Denver, CO' found in preferred locations: {locations}"

    missing = []
    if not has_boston:
        missing.append("Boston, MA")
    if not has_denver:
        missing.append("Denver, CO")
    return False, (
        f"Missing locations: {missing}. Current preferred locations: {locations}"
    )
