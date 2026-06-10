import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # 1. Check Advisory Call booking page exists
    advisory = None
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Advisory Call":
            advisory = bp
            break

    if not advisory:
        errors.append("Booking page 'Advisory Call' not found.")
    else:
        if advisory.get("duration") != 45:
            errors.append(f"Advisory Call duration is {advisory.get('duration')}, expected 45.")
        loc = (advisory.get("location") or "").lower()
        if "google meet" not in loc:
            errors.append(f"Advisory Call location is '{advisory.get('location')}', expected Google Meet.")
        avail = advisory.get("availability", {})
        days = avail.get("days", [])
        if set(days) != {"Wed", "Fri"}:
            errors.append(f"Advisory Call days: {days}, expected ['Wed', 'Fri'].")
        if avail.get("startTime") != "14:00":
            errors.append(f"Advisory Call start: {avail.get('startTime')}, expected 14:00.")
        if avail.get("endTime") != "17:00":
            errors.append(f"Advisory Call end: {avail.get('endTime')}, expected 17:00.")

    # 2. Check Product Demo booking page is gone
    for bp in state.get("bookingPages", []):
        if bp.get("title") == "Product Demo":
            errors.append("Product Demo booking page still exists.")
            break

    # 3. Check Advisory auto label exists
    advisory_al = None
    for al in state.get("autoLabels", []):
        if al.get("name") == "Advisory":
            advisory_al = al
            break

    if not advisory_al:
        errors.append("Auto label 'Advisory' not found.")
    else:
        if advisory_al.get("type") != "custom":
            errors.append(f"Advisory auto label type is '{advisory_al.get('type')}', expected 'custom'.")
        criteria = advisory_al.get("criteria", {})
        subj = (criteria.get("subject") or "").lower()
        if "advisory" not in subj or "consulting" not in subj:
            errors.append(f"Advisory auto label subject criteria: '{criteria.get('subject')}', expected advisory and consulting.")

    if errors:
        return False, " ".join(errors)

    return True, "Advisory Call booking page created, Product Demo deleted, Advisory auto label created."
