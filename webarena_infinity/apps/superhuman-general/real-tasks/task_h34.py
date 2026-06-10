import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    labels = state.get("labels", [])
    label_names = {l["name"] for l in labels}

    errors = []

    # Check that "Events" label is deleted
    if "Events" in label_names:
        errors.append("Label 'Events' still exists.")

    # Check that "Newsletters" label is deleted
    if "Newsletters" in label_names:
        errors.append("Label 'Newsletters' still exists.")

    # Also verify no emails still reference the old label IDs
    # Events = label_14, Newsletters = label_7
    for e in state.get("emails", []):
        email_labels = e.get("labels", [])
        if "label_14" in email_labels:
            errors.append(f"Email '{e.get('subject', '?')}' still has Events label (label_14).")
        if "label_7" in email_labels:
            errors.append(f"Email '{e.get('subject', '?')}' still has Newsletters label (label_7).")

    if errors:
        return False, " ".join(errors[:3])  # Limit error message length

    return True, "Labels 'Events' and 'Newsletters' have been deleted and removed from all emails."
