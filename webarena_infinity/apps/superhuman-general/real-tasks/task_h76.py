import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Quick Sync and Product Demo should be gone
    for bp in state.get("bookingPages", []):
        if bp.get("title") in ("Quick Sync", "Product Demo"):
            errors.append(f"Booking page '{bp['title']}' still exists.")

    # Office Hours should exist
    office = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Office Hours":
            office = bp
            break

    if not office:
        errors.append("Booking page 'Office Hours' not found.")
    else:
        if office.get("duration") != 30:
            errors.append(f"Office Hours duration is {office.get('duration')}, expected 30.")
        loc = (office.get("location") or "").lower()
        if "zoom" not in loc:
            errors.append(f"Office Hours location is '{office.get('location')}', expected Zoom.")
        avail = office.get("availability", {})
        days = set(avail.get("days", []))
        expected_days = {"Mon", "Tue", "Wed", "Thu", "Fri"}
        if days != expected_days:
            errors.append(f"Office Hours days: {avail.get('days')}, expected Mon-Fri.")
        if avail.get("startTime") != "09:00":
            errors.append(f"Office Hours start: {avail.get('startTime')}, expected 09:00.")
        if avail.get("endTime") != "12:00":
            errors.append(f"Office Hours end: {avail.get('endTime')}, expected 12:00.")

    if errors:
        return False, " ".join(errors)

    return True, "Quick Sync and Product Demo deleted; Office Hours created correctly."
