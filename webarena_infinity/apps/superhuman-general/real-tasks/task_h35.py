import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find "Chat with Alex" booking page
    chat_page = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Chat with Alex":
            chat_page = bp
            break
    if not chat_page:
        return False, "Booking page 'Chat with Alex' not found."

    errors = []

    # Check duration
    if chat_page.get("duration") != 45:
        errors.append(f"Duration is {chat_page.get('duration')}, expected 45.")

    # Check availability days (Mon-Fri)
    avail = chat_page.get("availability", {})
    days = avail.get("days", [])
    normalized_days = {d[:3].lower() for d in days}
    expected_days = {"mon", "tue", "wed", "thu", "fri"}
    if normalized_days != expected_days:
        errors.append(f"Availability days are {days}, expected Mon-Fri.")

    # Check start and end time
    if avail.get("startTime") != "10:00":
        errors.append(f"Start time is '{avail.get('startTime')}', expected '10:00'.")
    if avail.get("endTime") != "16:00":
        errors.append(f"End time is '{avail.get('endTime')}', expected '16:00'.")

    if errors:
        return False, " ".join(errors)

    return True, "Booking page 'Chat with Alex' updated: 45 min, Mon-Fri, 10am-4pm."
