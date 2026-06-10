# Task: VIP Clients contacts — starred ones get Emergency, unstarred get starred.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Seed VIP Clients (clabel_4):
    # Sarah Chen (starred -> add Emergency)
    # Emily Rodriguez (starred -> add Emergency)
    # David Kim (not starred -> star)
    # Ryan Cooper (not starred -> star)
    contacts = state.get("contacts", [])

    starred_vips = [("Sarah", "Chen"), ("Emily", "Rodriguez")]
    unstarred_vips = [("David", "Kim"), ("Ryan", "Cooper")]

    for first, last in starred_vips:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
        else:
            if "clabel_10" not in contact.get("labels", []):
                errors.append(f"{first} {last} should have the Emergency label")

    for first, last in unstarred_vips:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
        else:
            if not contact.get("isStarred"):
                errors.append(f"{first} {last} should be starred")

    if errors:
        return False, "; ".join(errors)
    return True, "VIP Clients: starred got Emergency, unstarred got starred."
