import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Design Review Follow-up" event
    event = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Design Review Follow-up":
            event = evt
            break
    if not event:
        return False, "Calendar event 'Design Review Follow-up' not found."

    errors = []

    # Verify date
    if event.get("date") != "2026-03-15":
        errors.append(f"Date is '{event.get('date')}', expected '2026-03-15'.")

    # Verify time
    if event.get("startTime") != "14:00":
        errors.append(f"Start time is '{event.get('startTime')}', expected '14:00'.")
    if event.get("endTime") != "15:00":
        errors.append(f"End time is '{event.get('endTime')}', expected '15:00'.")

    # Verify location contains Zoom
    location = (event.get("location") or "").lower()
    if "zoom" not in location:
        errors.append(f"Location is '{event.get('location')}', expected to contain 'Zoom'.")

    # Verify attendees from Design Review event (evt_9):
    # marcus.w@designhub.io and maya.patel@acmecorp.com
    attendees = event.get("attendees", [])
    attendee_emails = set()
    for a in attendees:
        if isinstance(a, dict):
            attendee_emails.add(a.get("email", ""))
        elif isinstance(a, str):
            attendee_emails.add(a)

    required = {"marcus.w@designhub.io", "maya.patel@acmecorp.com"}
    missing = required - attendee_emails
    if missing:
        errors.append(f"Missing attendees: {', '.join(missing)}. Current attendees: {attendees}")

    if errors:
        return False, " ".join(errors)

    return True, "Calendar event 'Design Review Follow-up' created with correct date, time, location, and attendees from Design Review."
