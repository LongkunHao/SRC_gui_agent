# Task: Find all contacts with July birthday, add VIP Clients label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # July birthday contacts: David Kim (07-19), Kevin Zhao (07-04),
    # Patricia Wong-Anderson (07-08), Jake Morrison (07-22)
    july_contacts = [
        ("David", "Kim"),
        ("Kevin", "Zhao"),
        ("Patricia", "Wong-Anderson"),
        ("Jake", "Morrison"),
    ]

    contacts = state.get("contacts", [])
    for first, last in july_contacts:
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
    return True, "All July birthday contacts have the VIP Clients label."
