import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find calendar event "Weekly Review"
    event = None
    for ev in state.get("calendarEvents", []):
        if ev.get("title") == "Weekly Review":
            event = ev
            break
    if not event:
        return False, "Calendar event 'Weekly Review' not found."

    # Check date is March 13, 2026
    event_date = event.get("date", "")
    if event_date != "2026-03-13":
        return False, f"Event date is '{event_date}', expected '2026-03-13'."

    # Check time 4-5pm
    start_time = event.get("startTime", "")
    end_time = event.get("endTime", "")
    if start_time != "16:00":
        return False, f"Start time is '{start_time}', expected '16:00'."
    if end_time != "17:00":
        return False, f"End time is '{end_time}', expected '17:00'."

    # Check location contains Zoom
    location = event.get("location", "")
    if "zoom" not in location.lower():
        return False, f"Location is '{location}', expected to contain 'Zoom'."

    # Check attendees include sarah.chen@acmecorp.com and nate.patel@acmecorp.com
    attendees = event.get("attendees", [])
    attendee_emails = []
    for a in attendees:
        if isinstance(a, dict):
            attendee_emails.append(a.get("email", "").lower())
        elif isinstance(a, str):
            attendee_emails.append(a.lower())

    if "sarah.chen@acmecorp.com" not in attendee_emails:
        return False, f"sarah.chen@acmecorp.com not found in attendees: {attendee_emails}."
    if "nate.patel@acmecorp.com" not in attendee_emails:
        return False, f"nate.patel@acmecorp.com not found in attendees: {attendee_emails}."

    return True, "Calendar event 'Weekly Review' created correctly on March 13, 4-5pm, Zoom, with Sarah Chen and Nate Patel."
