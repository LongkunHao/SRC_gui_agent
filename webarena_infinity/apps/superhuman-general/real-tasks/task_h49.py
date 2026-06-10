import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Team Offsite (evt_14, March 12) attendees:
    # sarah.chen, nate.patel, maya.patel, tom.bradley, ben.carter, rachel.foster
    offsite_attendees = set()
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Team Offsite":
            for a in evt.get("attendees", []):
                if isinstance(a, dict):
                    offsite_attendees.add(a.get("email", ""))
                elif isinstance(a, str):
                    offsite_attendees.add(a)
            break

    if not offsite_attendees:
        return False, "Could not find Team Offsite event or its attendees."

    # Find all unread inbox emails from offsite attendees and check they're starred
    errors = []
    starred_count = 0
    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if (sender in offsite_attendees
                and not e.get("isDone") and not e.get("isTrashed")
                and not e.get("isSpam") and not e.get("isDraft")
                and e.get("remindAt") is None
                and not e.get("isRead")):
            if not e.get("isStarred"):
                errors.append(f"Unread email '{e['subject']}' from {sender} is not starred.")
            else:
                starred_count += 1

    if errors:
        return False, " ".join(errors)

    if starred_count == 0:
        return False, "No unread inbox emails from Team Offsite attendees were found starred."

    return True, f"{starred_count} unread inbox email(s) from Team Offsite attendees starred."
