# Task: Delete EuroDesign contacts, dismiss EuroDesign merge, delete Travel Contacts label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    merge_suggestions = state.get("mergeSuggestions", [])
    contact_labels = state.get("contactLabels", [])

    # Sophie Laurent and Elena Volkov should be deleted
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        if name in ("Sophie Laurent", "Elena Volkov"):
            errors.append(f"EuroDesign contact '{name}' still exists")

    # merge_2 (EuroDesign) should be dismissed
    for ms in merge_suggestions:
        if ms.get("id") == "merge_2":
            if not ms.get("dismissed"):
                errors.append("EuroDesign merge suggestion (merge_2) not dismissed")
            break
    else:
        errors.append("merge_2 not found in mergeSuggestions")

    # Travel Contacts label (clabel_11) should be deleted
    for lbl in contact_labels:
        if lbl.get("id") == "clabel_11" or lbl.get("name") == "Travel Contacts":
            errors.append("Travel Contacts label still exists")

    # No contact should reference clabel_11
    for c in contacts:
        if "clabel_11" in c.get("labels", []):
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            errors.append(f"Contact '{name}' still has Travel Contacts label")

    if errors:
        return False, "; ".join(errors)
    return True, "EuroDesign contacts deleted, merge dismissed, Travel Contacts label removed."
