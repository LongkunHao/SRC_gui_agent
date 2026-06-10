import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check merge_1 is dismissed
    merge_suggestions = state.get("mergeSuggestions", [])
    merge_1 = None
    for ms in merge_suggestions:
        if ms.get("id") == "merge_1":
            merge_1 = ms
            break

    if merge_1 is None:
        return False, "Merge suggestion 'merge_1' not found."

    if not merge_1.get("dismissed"):
        return False, f"Merge suggestion 'merge_1' is not dismissed. dismissed={merge_1.get('dismissed')}."

    # Check contact_36 (Raj Kapoor) no longer exists
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("id") == "contact_36":
            return False, "Contact 'contact_36' (Raj Kapoor) still exists after merge."

    # Check contact_05 (Priya Sharma) still exists
    priya_found = False
    for contact in contacts:
        if contact.get("id") == "contact_05":
            priya_found = True
            break

    if not priya_found:
        return False, "Primary contact 'contact_05' (Priya Sharma) no longer exists."

    return True, "Merge suggestion 'merge_1' is dismissed, contact_36 (Raj Kapoor) removed, and contact_05 (Priya Sharma) still exists."
