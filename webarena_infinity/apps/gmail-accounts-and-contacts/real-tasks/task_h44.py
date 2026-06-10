# Task: Find sister's husband, star him, add Friends label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Leo Martinez is the sister's husband (Laura Johnson-Martinez's husband)
    leo = None
    for c in contacts:
        if c.get("firstName") == "Leo" and c.get("lastName") == "Martinez":
            leo = c
            break

    if leo is None:
        errors.append("Leo Martinez not found")
    else:
        if not leo.get("isStarred"):
            errors.append("Leo Martinez should be starred")
        if "clabel_2" not in leo.get("labels", []):
            errors.append("Leo Martinez should have the Friends label")

    if errors:
        return False, "; ".join(errors)
    return True, "Leo Martinez (sister's husband) starred and Friends label added."
