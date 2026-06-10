import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Emails that originally had remindAt set: ids 64, 65, 66, 67, 111, 112
    reminder_ids = [64, 65, 66, 67, 111, 112]

    emails_by_id = {}
    for e in state.get("emails", []):
        emails_by_id[e["id"]] = e

    still_have_reminders = []
    for eid in reminder_ids:
        email = emails_by_id.get(eid)
        if not email:
            continue  # Email might have been removed; acceptable
        remind_at = email.get("remindAt")
        if remind_at is not None:
            still_have_reminders.append(f"id={eid} subject='{email.get('subject', '?')}' remindAt='{remind_at}'")

    if still_have_reminders:
        return False, f"The following emails still have reminders set: {'; '.join(still_have_reminders)}."

    return True, "All reminders have been cleared from snoozed emails."
