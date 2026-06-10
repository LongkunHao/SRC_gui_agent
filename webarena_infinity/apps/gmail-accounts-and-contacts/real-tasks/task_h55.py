# Task: Add VIP Clients to all contacts on Sand Hill Rd.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Sand Hill Rd contacts: Sarah Chen, Maya Patel, Patricia Wong-Anderson
    sand_hill_contacts = [
        ("Sarah", "Chen"),            # already has VIP Clients
        ("Maya", "Patel"),            # needs VIP Clients
        ("Patricia", "Wong-Anderson"),  # needs VIP Clients
    ]

    for first, last in sand_hill_contacts:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
            continue
        if "clabel_4" not in contact.get("labels", []):
            errors.append(
                f"{first} {last} should have VIP Clients label "
                "(address on Sand Hill Rd)"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "All Sand Hill Rd contacts have VIP Clients label."
