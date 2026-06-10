# Task: Two contacts with last name Chen — delete the dentist, update the other's title.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Mike Chen (Dentist) should be deleted
    for c in contacts:
        if c.get("firstName") == "Mike" and c.get("lastName") == "Chen":
            errors.append("Mike Chen (dentist) should have been deleted")

    # Sarah Chen should have updated job title
    sarah = None
    for c in contacts:
        if c.get("firstName") == "Sarah" and c.get("lastName") == "Chen":
            sarah = c
            break

    if sarah is None:
        errors.append("Sarah Chen not found (should not have been deleted)")
    elif sarah.get("jobTitle") != "Chief Product Officer":
        errors.append(
            f"Sarah Chen's job title is '{sarah.get('jobTitle')}' "
            "instead of 'Chief Product Officer'"
        )

    if errors:
        return False, "; ".join(errors)
    return True, "Mike Chen deleted, Sarah Chen updated to Chief Product Officer."
