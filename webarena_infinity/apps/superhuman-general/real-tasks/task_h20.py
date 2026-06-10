import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the Travel label
    travel_label = None
    for label in state.get("labels", []):
        if label["name"] == "Travel":
            travel_label = label
            break
    if not travel_label:
        return False, "Label 'Travel' not found."
    travel_id = travel_label["id"]

    # Find all emails with the Travel label
    travel_emails = []
    for e in state.get("emails", []):
        if travel_id in e.get("labels", []):
            travel_emails.append(e)

    if not travel_emails:
        return False, f"No emails found with the 'Travel' label (id={travel_id})."

    # Check all Travel-labeled emails are marked as done
    not_done = []
    for e in travel_emails:
        if not e.get("isDone", False):
            not_done.append(f"id={e['id']} subject='{e.get('subject', '?')}'")

    if not_done:
        return False, f"{len(not_done)} Travel email(s) not archived: {'; '.join(not_done)}."

    return True, f"All {len(travel_emails)} emails with 'Travel' label have been moved to Done."
