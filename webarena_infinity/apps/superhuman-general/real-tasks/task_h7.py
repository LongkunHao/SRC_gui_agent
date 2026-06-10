import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find booking page with title "Strategy Session"
    booking_page = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Strategy Session":
            booking_page = bp
            break
    if not booking_page:
        return False, "Booking page 'Strategy Session' not found."

    # Check duration
    if booking_page.get("duration") != 60:
        return False, f"Duration is {booking_page.get('duration')}, expected 60 minutes."

    # Check location contains Google Meet
    location = booking_page.get("location", "")
    if "google meet" not in location.lower() and "google_meet" not in location.lower() and "googlemeet" not in location.lower():
        return False, f"Location is '{location}', expected to contain 'Google Meet'."

    # Check availability
    availability = booking_page.get("availability", {})
    days = availability.get("days", [])

    required_days = {"Monday", "Tuesday", "Wednesday", "Thursday"}
    # Normalize day names to handle abbreviations
    normalized_days = set()
    for d in days:
        d_lower = d.lower()
        if d_lower in ("mon", "monday"):
            normalized_days.add("Monday")
        elif d_lower in ("tue", "tuesday"):
            normalized_days.add("Tuesday")
        elif d_lower in ("wed", "wednesday"):
            normalized_days.add("Wednesday")
        elif d_lower in ("thu", "thursday"):
            normalized_days.add("Thursday")
        elif d_lower in ("fri", "friday"):
            normalized_days.add("Friday")
        else:
            normalized_days.add(d)

    if not required_days.issubset(normalized_days):
        missing = required_days - normalized_days
        return False, f"Missing required days: {missing}. Current days: {days}."
    if "Friday" in normalized_days:
        return False, f"Friday should not be included in availability. Current days: {days}."

    # Check time range
    start_time = availability.get("startTime", "")
    end_time = availability.get("endTime", "")
    if start_time != "13:00":
        return False, f"Start time is '{start_time}', expected '13:00'."
    if end_time != "17:00":
        return False, f"End time is '{end_time}', expected '17:00'."

    return True, "Booking page 'Strategy Session' created correctly with 60 min, Google Meet, Mon-Thu 1-5pm."
