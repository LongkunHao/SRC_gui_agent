# Task: Find contact with 'spare key' in notes, star, add Family, change phone.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    ben = None
    for c in contacts:
        if c.get("firstName") == "Ben" and c.get("lastName") == "Walker":
            ben = c
            break

    if ben is None:
        errors.append("Ben Walker not found")
    else:
        if not ben.get("isStarred"):
            errors.append("Ben Walker should be starred")
        if "clabel_1" not in ben.get("labels", []):
            errors.append("Ben Walker should have the Family label")
        if ben.get("phone") != "+1 (415) 555-9911":
            errors.append(
                f"Phone is '{ben.get('phone')}' instead of '+1 (415) 555-9911'"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Ben Walker starred, Family label added, phone updated."
