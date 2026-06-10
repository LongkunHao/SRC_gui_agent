import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # 1. Check "Board Prep" booking page exists with correct settings
    board_prep = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Board Prep":
            board_prep = bp
            break
    if not board_prep:
        return False, "Booking page 'Board Prep' not found."

    if board_prep.get("duration") != 90:
        return False, f"Board Prep duration is {board_prep.get('duration')}, expected 90."

    location = (board_prep.get("location") or "").lower()
    if "zoom" not in location:
        return False, f"Board Prep location is '{board_prep.get('location')}', expected to contain 'Zoom'."

    avail = board_prep.get("availability", {})
    days = [d.lower() if isinstance(d, str) else d for d in avail.get("days", [])]
    required_days = {"tue", "thu"}
    actual_days = {d[:3] for d in days}
    if not required_days.issubset(actual_days):
        return False, f"Board Prep availability days are {avail.get('days')}, expected Tue and Thu."

    if avail.get("startTime") != "09:00":
        return False, f"Board Prep start time is '{avail.get('startTime')}', expected '09:00'."
    if avail.get("endTime") != "12:00":
        return False, f"Board Prep end time is '{avail.get('endTime')}', expected '12:00'."

    if not board_prep.get("isActive", True):
        return False, "Board Prep should be active."

    # 2. Check "Chat with Alex" is deactivated
    chat_page = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Chat with Alex":
            chat_page = bp
            break
    if not chat_page:
        return False, "Booking page 'Chat with Alex' not found."
    if chat_page.get("isActive", True):
        return False, "Booking page 'Chat with Alex' should be deactivated but is still active."

    return True, "Booking page 'Board Prep' created and 'Chat with Alex' deactivated."
