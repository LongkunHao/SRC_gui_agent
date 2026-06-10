import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find calendar event with title "Team Lunch"
    target_event = None
    for event in state.get("calendarEvents", []):
        if event.get("title") == "Team Lunch":
            target_event = event
            break

    if not target_event:
        return False, "Could not find a calendar event titled 'Team Lunch'."

    errors = []

    # Check date
    if target_event.get("date") != "2026-03-13":
        errors.append(f"Date is '{target_event.get('date')}', expected '2026-03-13'.")

    # Check start time
    if target_event.get("startTime") != "12:00":
        errors.append(f"Start time is '{target_event.get('startTime')}', expected '12:00'.")

    # Check end time
    if target_event.get("endTime") != "13:00":
        errors.append(f"End time is '{target_event.get('endTime')}', expected '13:00'.")

    # Check location contains Café Roma or Cafe Roma
    location = target_event.get("location", "")
    if "café roma" not in location.lower() and "cafe roma" not in location.lower():
        errors.append(f"Location is '{location}', expected it to contain 'Café Roma' or 'Cafe Roma'.")

    if errors:
        return False, "Team Lunch event found but has issues: " + " ".join(errors)

    return True, "Calendar event 'Team Lunch' created correctly on March 13, 12-1pm at Café Roma."
