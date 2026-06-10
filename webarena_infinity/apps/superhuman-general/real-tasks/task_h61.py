import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Contract Signing" event
    event = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Contract Signing":
            event = evt
            break
    if not event:
        return False, "Calendar event 'Contract Signing' not found."

    # Check date
    if event.get("date") != "2026-03-14":
        return False, f"Event date is '{event.get('date')}', expected '2026-03-14'."

    # Check times
    if event.get("startTime") != "10:00":
        return False, f"Start time is '{event.get('startTime')}', expected '10:00'."
    if event.get("endTime") != "11:00":
        return False, f"End time is '{event.get('endTime')}', expected '11:00'."

    # Check location contains Zoom
    loc = (event.get("location") or "").lower()
    if "zoom" not in loc:
        return False, f"Location is '{event.get('location')}', expected Zoom."

    # Check attendees: James O'Brien (attorney) and Michael Foster (CloudScale)
    attendees = set()
    for a in event.get("attendees", []):
        if isinstance(a, dict):
            attendees.add(a.get("email", ""))
        elif isinstance(a, str):
            attendees.add(a)

    required = {"james.obrien@legalwise.com", "michael.f@cloudscale.dev"}
    missing = required - attendees
    if missing:
        return False, f"Missing attendees: {', '.join(missing)}. Found: {', '.join(attendees)}"

    return True, "Event 'Contract Signing' created correctly with both attendees."
