# Task: Add VIP Clients to all contacts with 'Director' in job title.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Contacts with 'Director' in job title:
    # Marcus Williams (Creative Director), Ana Gutierrez (Community Outreach Director),
    # Sophie Laurent (Conference Director), Jennifer Wu (Director of Research),
    # Rachel Foster (Executive Director)
    director_contacts = [
        ("Marcus", "Williams"),
        ("Ana", "Gutierrez"),
        ("Sophie", "Laurent"),
        ("Jennifer", "Wu"),
        ("Rachel", "Foster"),
    ]

    contacts = state.get("contacts", [])
    for first, last in director_contacts:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
        elif "clabel_4" not in contact.get("labels", []):
            errors.append(f"{first} {last} does not have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "All Director contacts have the VIP Clients label."
