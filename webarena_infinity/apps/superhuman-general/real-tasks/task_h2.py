import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # The originally unread important inbox emails: ids 1, 2, 3, 5, 113, 114
    target_ids = [1, 2, 3, 5, 113, 114]

    emails_by_id = {}
    for e in state.get("emails", []):
        emails_by_id[e["id"]] = e

    not_archived = []
    for eid in target_ids:
        email = emails_by_id.get(eid)
        if not email:
            return False, f"Email with id {eid} not found in state."
        if not email.get("isDone", False):
            not_archived.append(f"id={eid} subject='{email.get('subject', '?')}'")

    if not_archived:
        return False, f"The following emails are not archived (isDone!=true): {'; '.join(not_archived)}."

    return True, "All unread important inbox emails have been archived."
