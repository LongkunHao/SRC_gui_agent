# Task: Create Portland label and add to contacts with Portland in address.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contact_labels = state.get("contactLabels", [])
    contacts = state.get("contacts", [])

    # Check Portland label exists with correct color
    portland_label = None
    for lbl in contact_labels:
        if lbl.get("name") == "Portland":
            portland_label = lbl
            break

    if portland_label is None:
        errors.append("Label 'Portland' not found")
    else:
        if portland_label.get("color") != "#009688":
            errors.append(
                f"Portland label color is '{portland_label.get('color')}' "
                "instead of '#009688'"
            )

    # Rachel Foster and Leo Martinez have Portland in their address
    should_have = [("Rachel", "Foster"), ("Leo", "Martinez")]

    if portland_label:
        label_id = portland_label.get("id")
        for first, last in should_have:
            contact = None
            for c in contacts:
                if c.get("firstName") == first and c.get("lastName") == last:
                    contact = c
                    break
            if contact is None:
                errors.append(f"{first} {last} not found")
                continue
            if label_id not in contact.get("labels", []):
                errors.append(
                    f"{first} {last} should have Portland label "
                    "(address contains Portland)"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Portland label created and assigned to Portland-area contacts."
