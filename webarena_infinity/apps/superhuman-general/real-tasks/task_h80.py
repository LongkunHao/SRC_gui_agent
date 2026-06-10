import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # 1. Check Priority Clients label
    pc_label = None
    for label in state.get("labels", []):
        if label["name"] == "Priority Clients":
            pc_label = label
            break

    if not pc_label:
        return False, "Label 'Priority Clients' not found."

    color = (pc_label.get("color") or "").lower()
    red_colors = [
        "#f44336", "#e53935", "#d32f2f", "#c62828", "#b71c1c",
        "#ff1744", "#ff5252", "#ef5350", "#e57373", "#ff0000",
        "red", "#ff5722", "#e53e3e",
    ]
    if color not in red_colors:
        errors.append(f"Label color is '{color}', expected red.")

    pc_id = pc_label["id"]

    # 2. Check FinancePlus and CloudScale inbox emails have the label
    target_senders = {
        "david.kim@financeplus.com": False,
        "michael.f@cloudscale.dev": False,
    }

    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if sender in target_senders:
            if (not e.get("isDone") and not e.get("isTrashed")
                    and not e.get("isSpam") and not e.get("isDraft")
                    and e.get("remindAt") is None):
                if pc_id in e.get("labels", []):
                    target_senders[sender] = True

    missing_labels = [s for s, found in target_senders.items() if not found]
    if missing_labels:
        errors.append(f"Missing 'Priority Clients' label on inbox emails from: {', '.join(missing_labels)}")

    # 3. Check Client Sync event
    event = None
    for evt in state.get("calendarEvents", []):
        if evt.get("title") == "Client Sync":
            event = evt
            break

    if not event:
        errors.append("Calendar event 'Client Sync' not found.")
    else:
        if event.get("date") != "2026-03-13":
            errors.append(f"Event date is '{event.get('date')}', expected '2026-03-13'.")
        if event.get("startTime") != "15:00":
            errors.append(f"Event start is '{event.get('startTime')}', expected '15:00'.")
        if event.get("endTime") != "16:00":
            errors.append(f"Event end is '{event.get('endTime')}', expected '16:00'.")
        loc = (event.get("location") or "").lower()
        if "zoom" not in loc:
            errors.append(f"Event location is '{event.get('location')}', expected Zoom.")

        attendees = set()
        for a in event.get("attendees", []):
            if isinstance(a, dict):
                attendees.add(a.get("email", ""))
            elif isinstance(a, str):
                attendees.add(a)

        req_attendees = {"david.kim@financeplus.com", "michael.f@cloudscale.dev"}
        missing_att = req_attendees - attendees
        if missing_att:
            errors.append(f"Missing event attendees: {', '.join(missing_att)}")

    if errors:
        return False, " ".join(errors)

    return True, "Priority Clients label applied and Client Sync event created with correct attendees."
