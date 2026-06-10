# Task: Find contact with 'office renovation' in notes, star, add Friends and VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    daniel = None
    for c in contacts:
        if c.get("firstName") == "Daniel" and c.get("lastName") == "Thompson":
            daniel = c
            break

    if daniel is None:
        errors.append("Daniel Thompson not found")
    else:
        if not daniel.get("isStarred"):
            errors.append("Daniel Thompson should be starred")
        if "clabel_2" not in daniel.get("labels", []):
            errors.append("Daniel Thompson should have the Friends label")
        if "clabel_4" not in daniel.get("labels", []):
            errors.append("Daniel Thompson should have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Daniel Thompson starred with Friends and VIP Clients labels."
