import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the Urgent label
    urgent_label = None
    for label in state.get("labels", []):
        if label["name"] == "Urgent":
            urgent_label = label
            break
    if not urgent_label:
        return False, "Label 'Urgent' not found."
    urgent_id = urgent_label["id"]

    # Find all inbox emails with attachments
    # Inbox = not done, not trashed, not spam, not draft, no remindAt
    inbox_with_attachments = []
    missing_label = []
    for e in state.get("emails", []):
        if (not e.get("isDone") and not e.get("isTrashed") and not e.get("isSpam")
                and not e.get("isDraft") and e.get("remindAt") is None
                and e.get("hasAttachments")):
            inbox_with_attachments.append(e)
            if urgent_id not in e.get("labels", []):
                missing_label.append(f"id={e['id']} subject='{e.get('subject', '?')}'")

    if not inbox_with_attachments:
        return False, "No inbox emails with attachments found."

    if missing_label:
        return False, f"{len(missing_label)} inbox email(s) with attachments missing 'Urgent' label: {'; '.join(missing_label)}"

    return True, f"All {len(inbox_with_attachments)} inbox emails with attachments have the 'Urgent' label."
