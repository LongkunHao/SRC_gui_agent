import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the Client Review event
    event = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Client Review":
            event = evt
            break
    if not event:
        return False, "Calendar event 'Client Review' not found."

    # Verify date
    if event.get("date") != "2026-03-11":
        return False, f"Event date is '{event.get('date')}', expected '2026-03-11'."

    # Verify time
    if event.get("startTime") != "14:00":
        return False, f"Start time is '{event.get('startTime')}', expected '14:00'."
    if event.get("endTime") != "15:00":
        return False, f"End time is '{event.get('endTime')}', expected '15:00'."

    # Verify location contains Zoom
    location = (event.get("location") or "").lower()
    if "zoom" not in location:
        return False, f"Location is '{event.get('location')}', expected to contain 'Zoom'."

    # Verify attendees include the senders of Clients-labeled inbox emails
    # David Kim (david.kim@financeplus.com) and Jennifer Wu (jennifer.wu@biomedresearch.com)
    attendees = event.get("attendees", [])
    attendee_emails = set()
    for a in attendees:
        if isinstance(a, dict):
            attendee_emails.add(a.get("email", ""))
        elif isinstance(a, str):
            attendee_emails.add(a)

    required = {"david.kim@financeplus.com", "jennifer.wu@biomedresearch.com"}
    missing = required - attendee_emails
    if missing:
        return False, f"Missing attendees: {', '.join(missing)}. Current attendees: {attendees}"

    return True, "Calendar event 'Client Review' created with correct date, time, location, and attendees."
