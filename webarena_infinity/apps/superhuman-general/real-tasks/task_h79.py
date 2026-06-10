import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Weekly Standup organizer: tom.bradley@acmecorp.com

    event = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Security Review":
            event = evt
            break

    if not event:
        return False, "Calendar event 'Security Review' not found."

    if event.get("date") != "2026-03-13":
        return False, f"Event date is '{event.get('date')}', expected '2026-03-13'."

    if event.get("startTime") != "11:00":
        return False, f"Start time is '{event.get('startTime')}', expected '11:00'."
    if event.get("endTime") != "12:00":
        return False, f"End time is '{event.get('endTime')}', expected '12:00'."

    loc = (event.get("location") or "").lower()
    if "zoom" not in loc:
        return False, f"Location is '{event.get('location')}', expected Zoom."

    attendees = set()
    for a in event.get("attendees", []):
        if isinstance(a, dict):
            attendees.add(a.get("email", ""))
        elif isinstance(a, str):
            attendees.add(a)

    required = {"ben.carter@acmecorp.com", "tom.bradley@acmecorp.com"}
    missing = required - attendees
    if missing:
        return False, f"Missing attendees: {', '.join(missing)}. Found: {', '.join(attendees)}"

    return True, "Event 'Security Review' created with Ben Carter and Weekly Standup organizer."
