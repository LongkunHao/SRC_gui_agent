# Task: Change profile name, create Priority label with red color, add to Family contacts.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Check profile name
    current_user = state.get("currentUser", {})
    if current_user.get("name") != "Alex J. Johnson":
        errors.append(
            f"Profile name is '{current_user.get('name')}' instead of 'Alex J. Johnson'"
        )

    # Check Priority label exists with red color
    contact_labels = state.get("contactLabels", [])
    priority_label = None
    for lbl in contact_labels:
        if lbl.get("name") == "Priority":
            priority_label = lbl
            break

    if priority_label is None:
        errors.append("Label 'Priority' not found")
    else:
        if priority_label.get("color") != "#EA4335":
            errors.append(
                f"Priority label color is '{priority_label.get('color')}' instead of '#EA4335'"
            )

    # Check all Family contacts have the Priority label
    contacts = state.get("contacts", [])
    family_contacts = [
        ("Margaret", "Johnson"),
        ("Richard", "Johnson"),
        ("Laura", "Johnson-Martinez"),
        ("Leo", "Martinez"),
    ]

    if priority_label:
        priority_id = priority_label.get("id")
        for first, last in family_contacts:
            contact = None
            for c in contacts:
                if c.get("firstName") == first and c.get("lastName") == last:
                    contact = c
                    break
            if contact is None:
                errors.append(f"Family contact {first} {last} not found")
            elif priority_id not in contact.get("labels", []):
                errors.append(
                    f"{first} {last} (Family) does not have the Priority label"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Profile name updated, Priority label created and added to Family contacts."
