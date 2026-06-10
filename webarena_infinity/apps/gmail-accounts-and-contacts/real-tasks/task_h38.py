# Task: Create Bay Area label with #4285F4, add to Menlo Park contacts.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contact_labels = state.get("contactLabels", [])
    contacts = state.get("contacts", [])

    # Check Bay Area label exists with correct color
    bay_area_label = None
    for lbl in contact_labels:
        if lbl.get("name") == "Bay Area":
            bay_area_label = lbl
            break

    if bay_area_label is None:
        errors.append("Label 'Bay Area' not found")
    else:
        if bay_area_label.get("color") != "#4285F4":
            errors.append(
                f"Bay Area label color is '{bay_area_label.get('color')}' "
                "instead of '#4285F4'"
            )

    # Menlo Park contacts should have the Bay Area label:
    # Sarah Chen, Kevin Zhao, Maya Patel, Patricia Wong-Anderson
    menlo_park_contacts = [
        ("Sarah", "Chen"),
        ("Kevin", "Zhao"),
        ("Maya", "Patel"),
        ("Patricia", "Wong-Anderson"),
    ]

    if bay_area_label:
        label_id = bay_area_label.get("id")
        for first, last in menlo_park_contacts:
            contact = None
            for c in contacts:
                if c.get("firstName") == first and c.get("lastName") == last:
                    contact = c
                    break
            if contact is None:
                errors.append(f"{first} {last} not found")
            elif label_id not in contact.get("labels", []):
                errors.append(
                    f"{first} {last} (Menlo Park) does not have Bay Area label"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Bay Area label created and added to all Menlo Park contacts."
