# Task: Migrate Vendors to Work, then delete the Vendors label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    contact_labels = state.get("contactLabels", [])

    # Vendors label (clabel_9) should be deleted
    for lbl in contact_labels:
        if lbl.get("id") == "clabel_9" or lbl.get("name") == "Vendors":
            errors.append("Vendors label still exists")

    # No contact should still reference clabel_9
    for c in contacts:
        if "clabel_9" in c.get("labels", []):
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            errors.append(f"'{name}' still has Vendors label")

    # Former Vendors contacts should now have Work (clabel_3)
    former_vendors = [
        ("James", "O'Brien"),       # already had Work
        ("Tom", "Bradley"),          # needed Work added
        ("Carlos", "Mendez"),        # needed Work added
        ("Daniel", "Thompson"),      # needed Work added
        ("Greg", "Hoffman"),         # needed Work added
    ]

    for first, last in former_vendors:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
            continue
        if "clabel_3" not in contact.get("labels", []):
            errors.append(f"{first} {last} should have Work label")

    if errors:
        return False, "; ".join(errors)
    return True, "Vendors migrated to Work, Vendors label deleted."
