import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # The Quarterly OKR Review organizer is priya.sharma@acmecorp.com
    # Priya's inbox email is "Budget Approval Needed - Marketing Campaign"
    organizer_email = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Quarterly OKR Review":
            organizer_email = evt.get("organizer")
            break
    if not organizer_email:
        return False, "Could not find 'Quarterly OKR Review' calendar event."

    # Find the inbox email from the organizer
    target = None
    for e in state.get("emails", []):
        if (e["from"]["email"] == organizer_email
                and not e.get("isDone") and not e.get("isTrashed")
                and not e.get("isSpam") and not e.get("isDraft")
                and e.get("remindAt") is None):
            target = e
            break
    if not target:
        return False, f"No inbox email found from OKR Review organizer ({organizer_email})."

    if not target.get("isStarred"):
        return False, f"Email '{target['subject']}' from {organizer_email} is not starred."

    return True, f"Inbox email from OKR Review organizer ({organizer_email}) is starred."
