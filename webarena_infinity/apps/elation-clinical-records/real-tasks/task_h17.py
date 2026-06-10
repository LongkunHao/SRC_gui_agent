import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])

    # Find Washington (pat_008)
    washington = None
    for p in patients:
        if p.get("lastName") == "Washington":
            washington = p
            break

    # Find Wu (pat_012)
    wu = None
    for p in patients:
        if p.get("lastName") == "Wu":
            wu = p
            break

    errors = []

    if not washington:
        errors.append("Patient with lastName 'Washington' not found.")
    else:
        tags = washington.get("tags", [])
        if "Pediatric" in tags:
            errors.append(f"Washington still has 'Pediatric' tag. Current tags: {tags}")

    if not wu:
        errors.append("Patient with lastName 'Wu' not found.")
    else:
        tags = wu.get("tags", [])
        if "Pediatric" in tags:
            errors.append(f"Wu still has 'Pediatric' tag. Current tags: {tags}")

    if errors:
        return False, " ".join(errors)

    return True, "The 'Pediatric' tag has been removed from both Washington and Wu."
