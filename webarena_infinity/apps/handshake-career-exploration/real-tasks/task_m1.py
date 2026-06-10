import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    bio = state.get("currentUser", {}).get("bio", "")
    bio_lower = bio.lower()

    if "ai safety" in bio_lower or "alignment research" in bio_lower:
        return True, f"Bio successfully updated. Current bio: '{bio}'"
    return False, f"Bio does not mention 'AI safety' or 'alignment research'. Current bio: '{bio}'"
