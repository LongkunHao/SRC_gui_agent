# Task: Find 'book club co-organizer' in notes, remove Neighbors, add VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    samantha = None
    for c in contacts:
        if c.get("firstName") == "Samantha" and c.get("lastName") == "Lee":
            samantha = c
            break

    if samantha is None:
        errors.append("Samantha Lee not found")
    else:
        if "clabel_7" in samantha.get("labels", []):
            errors.append("Samantha Lee should not have the Neighbors label")
        if "clabel_4" not in samantha.get("labels", []):
            errors.append("Samantha Lee should have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Samantha Lee: Neighbors removed, VIP Clients added."
