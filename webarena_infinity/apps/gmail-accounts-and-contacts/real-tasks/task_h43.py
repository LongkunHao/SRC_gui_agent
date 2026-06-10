# Task: Disambiguate two Patels by delegate status, update title and add VIP label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Nate Patel (not a delegate) -> job title should be 'Senior Infrastructure Lead'
    nate = None
    for c in contacts:
        if c.get("firstName") == "Nate" and c.get("lastName") == "Patel":
            nate = c
            break
    if nate is None:
        errors.append("Nate Patel not found")
    elif nate.get("jobTitle") != "Senior Infrastructure Lead":
        errors.append(
            f"Nate Patel job title is '{nate.get('jobTitle')}' "
            "instead of 'Senior Infrastructure Lead'"
        )

    # Maya Patel (is a delegate) -> should have VIP Clients label (clabel_4)
    maya = None
    for c in contacts:
        if c.get("firstName") == "Maya" and c.get("lastName") == "Patel":
            maya = c
            break
    if maya is None:
        errors.append("Maya Patel not found")
    elif "clabel_4" not in maya.get("labels", []):
        errors.append("Maya Patel should have VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Patels updated: Nate title changed, Maya got VIP Clients."
