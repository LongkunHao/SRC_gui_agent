import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Engineering label
    eng_label = None
    for label in state.get("labels", []):
        if label["name"] == "Engineering":
            eng_label = label
            break
    if not eng_label:
        return False, "Label 'Engineering' not found."
    eng_id = eng_label["id"]

    # Find emails in Other split with Engineering label that are in inbox
    # Other split: splitCategory = 'other'
    # Inbox: not done, not trashed, not spam, not draft
    not_trashed = []
    trashed_count = 0
    for e in state.get("emails", []):
        if (e.get("splitCategory") == "other"
                and eng_id in e.get("labels", [])
                and not e.get("isSpam") and not e.get("isDraft")):
            if e.get("isTrashed"):
                trashed_count += 1
            elif not e.get("isDone"):
                not_trashed.append(f"id={e['id']} subject='{e.get('subject', '?')}'")

    if not_trashed:
        return False, f"{len(not_trashed)} Other/Engineering email(s) not trashed: {'; '.join(not_trashed[:3])}"

    if trashed_count == 0:
        return False, "No Other/Engineering emails found in trash."

    return True, f"All {trashed_count} Engineering-labeled emails from the Other split have been trashed."
