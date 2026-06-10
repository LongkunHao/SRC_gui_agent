import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find "Needs Response" label
    nr_label = None
    for label in state.get("labels", []):
        if label["name"] == "Needs Response":
            nr_label = label
            break
    if not nr_label:
        return False, "Label 'Needs Response' not found."
    if nr_label.get("type") != "user":
        return False, f"Label type is '{nr_label.get('type')}', expected 'user'."

    # Check color is purple-ish
    color = (nr_label.get("color") or "").lower()
    purple_colors = ["#9c27b0", "#7b1fa2", "#6a1b9a", "#4a148c", "#8e24aa",
                     "#ab47bc", "#ce93d8", "#ba68c8", "#9575cd", "#7e57c2",
                     "#673ab7", "#6c4ff7", "#5e35b1", "purple", "#800080"]
    if color not in purple_colors:
        return False, f"Label color is '{color}', expected a purple color."

    nr_id = nr_label["id"]

    # Find all unread emails in Important inbox split
    # Important split: splitCategory = 'important'
    # Inbox: not done, not trashed, not spam, not draft, no remindAt
    # Unread: isRead = false
    unread_important = []
    missing_label = []
    for e in state.get("emails", []):
        if (not e.get("isDone") and not e.get("isTrashed") and not e.get("isSpam")
                and not e.get("isDraft") and e.get("remindAt") is None
                and e.get("splitCategory") == "important" and not e.get("isRead")):
            unread_important.append(e)
            if nr_id not in e.get("labels", []):
                missing_label.append(f"id={e['id']} '{e.get('subject', '?')}'")

    if not unread_important:
        return False, "No unread emails found in the Important inbox split."

    if missing_label:
        return False, f"{len(missing_label)} unread Important email(s) missing 'Needs Response' label: {'; '.join(missing_label)}"

    return True, f"Label 'Needs Response' created with purple color and applied to all {len(unread_important)} unread Important inbox emails."
