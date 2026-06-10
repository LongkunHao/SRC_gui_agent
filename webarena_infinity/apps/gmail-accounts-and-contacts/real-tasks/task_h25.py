# Task: Find Priya Sharma's company, remove the Work label from all contacts at that company.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Priya Sharma works at CloudNine
    # CloudNine contacts: Priya Sharma (contact_05) and Raj Kapoor (contact_36)
    # Both should have Work label (clabel_3) removed

    cloudnine_contacts = [
        ("Priya", "Sharma"),
        ("Raj", "Kapoor"),
    ]

    for first, last in cloudnine_contacts:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found in contacts")
            continue
        if "clabel_3" in contact.get("labels", []):
            errors.append(
                f"{first} {last} (CloudNine) still has the Work label"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Work label removed from all CloudNine contacts."
