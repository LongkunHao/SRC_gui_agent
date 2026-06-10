import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    booking_pages = state.get("bookingPages", [])
    bp_map = {bp["title"]: bp for bp in booking_pages}
    errors = []

    # 1. "Investor Call" booking page should exist
    investor = bp_map.get("Investor Call")
    if not investor:
        errors.append("Booking page 'Investor Call' not found.")
    else:
        if investor.get("duration") != 30:
            errors.append(f"Duration is {investor.get('duration')}, expected 30.")
        location = (investor.get("location") or "").lower()
        if "zoom" not in location:
            errors.append(f"Location is '{investor.get('location')}', expected Zoom.")
        avail = investor.get("availability", {})
        days = [d.lower() if isinstance(d, str) else d for d in avail.get("days", [])]
        expected_days = {"mon", "tue", "wed", "thu", "fri"}
        actual_days = set(days)
        # Accept full names too
        full_name_map = {"monday": "mon", "tuesday": "tue", "wednesday": "wed",
                         "thursday": "thu", "friday": "fri"}
        actual_normalized = set()
        for d in actual_days:
            actual_normalized.add(full_name_map.get(d, d))
        if actual_normalized != expected_days:
            errors.append(f"Days are {avail.get('days')}, expected Mon-Fri.")
        if avail.get("startTime") != "14:00":
            errors.append(f"Start time is '{avail.get('startTime')}', expected '14:00'.")
        if avail.get("endTime") != "17:00":
            errors.append(f"End time is '{avail.get('endTime')}', expected '17:00'.")

    # 2. "Quick Sync" should be activated
    quick_sync = bp_map.get("Quick Sync")
    if not quick_sync:
        errors.append("Booking page 'Quick Sync' not found.")
    elif not quick_sync.get("isActive"):
        errors.append("'Quick Sync' booking page is not active (should be activated).")

    # 3. "Product Demo" should be deleted
    if "Product Demo" in bp_map:
        errors.append("'Product Demo' booking page still exists (should be deleted).")

    if errors:
        return False, " ".join(errors)

    return True, "Investor Call created, Quick Sync activated, Product Demo deleted."
