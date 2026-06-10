# Task: Personal trainer and yoga instructor — remove Gym Buddies, add Friends.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Hannah Brooks (Personal Trainer at FitnessFirst)
    hannah = None
    for c in contacts:
        if c.get("firstName") == "Hannah" and c.get("lastName") == "Brooks":
            hannah = c
            break
    if hannah is None:
        errors.append("Hannah Brooks not found")
    else:
        if "clabel_5" in hannah.get("labels", []):
            errors.append("Hannah Brooks should not have Gym Buddies label")
        if "clabel_2" not in hannah.get("labels", []):
            errors.append("Hannah Brooks should have the Friends label")

    # Diana Castillo (Yoga Instructor)
    diana = None
    for c in contacts:
        if c.get("firstName") == "Diana" and c.get("lastName") == "Castillo":
            diana = c
            break
    if diana is None:
        errors.append("Diana Castillo not found")
    else:
        if "clabel_5" in diana.get("labels", []):
            errors.append("Diana Castillo should not have Gym Buddies label")
        if "clabel_2" not in diana.get("labels", []):
            errors.append("Diana Castillo should have the Friends label")

    if errors:
        return False, "; ".join(errors)
    return True, "Trainer and instructor: Gym Buddies removed, Friends added."
