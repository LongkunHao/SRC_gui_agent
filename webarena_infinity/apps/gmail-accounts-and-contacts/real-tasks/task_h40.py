# Task: Create Key Contacts label, add to starred+VIP contacts, remove VIP from unstarred.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contact_labels = state.get("contactLabels", [])
    contacts = state.get("contacts", [])

    # Check Key Contacts label exists with correct color
    key_label = None
    for lbl in contact_labels:
        if lbl.get("name") == "Key Contacts":
            key_label = lbl
            break

    if key_label is None:
        errors.append("Label 'Key Contacts' not found")
    else:
        if key_label.get("color") != "#FBBC04":
            errors.append(
                f"Key Contacts label color is '{key_label.get('color')}' "
                "instead of '#FBBC04'"
            )

    # Sarah Chen and Emily Rodriguez (starred + VIP) should have Key Contacts
    should_have_key = ["Sarah Chen", "Emily Rodriguez"]
    contact_map = {}
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        contact_map[name] = c

    if key_label:
        key_id = key_label.get("id")
        for name in should_have_key:
            contact = contact_map.get(name)
            if contact is None:
                errors.append(f"Contact '{name}' not found")
            elif key_id not in contact.get("labels", []):
                errors.append(
                    f"'{name}' (starred + VIP) should have Key Contacts label"
                )

    # David Kim and Ryan Cooper (VIP but not starred) should lose VIP Clients (clabel_4)
    should_lose_vip = ["David Kim", "Ryan Cooper"]
    for name in should_lose_vip:
        contact = contact_map.get(name)
        if contact is None:
            errors.append(f"Contact '{name}' not found")
        elif "clabel_4" in contact.get("labels", []):
            errors.append(
                f"'{name}' (not starred) should have VIP Clients label removed"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Key Contacts label created, assigned to starred VIP contacts, VIP removed from unstarred."
