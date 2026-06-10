import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Meeting Prep" label
    mp_label = None
    for label in state.get("labels", []):
        if label["name"] == "Meeting Prep":
            mp_label = label
            break
    if not mp_label:
        return False, "Label 'Meeting Prep' not found."

    # Check color is green-ish
    color = (mp_label.get("color") or "").lower()
    green_colors = [
        "#4caf50", "#43a047", "#388e3c", "#2e7d32", "#1b5e20",
        "#66bb6a", "#81c784", "#a5d6a7", "#00c853", "#00e676",
        "#69f0ae", "#b9f6ca", "#8bc34a", "#7cb342", "#689f38",
        "#558b2f", "#33691e", "#76ff03", "#64dd17", "#4caf50",
        "green", "#34a853", "#2e7d32", "#009688", "#00bcd4",
    ]
    if color not in green_colors:
        return False, f"Label color is '{color}', expected a green color."

    mp_id = mp_label["id"]

    # Collect all people with calendar events on March 8
    march8_people = set()
    for evt in state.get("calendarEvents", []):
        if evt.get("date") == "2026-03-08":
            org = evt.get("organizer", "")
            if org:
                march8_people.add(org)
            for a in evt.get("attendees", []):
                if isinstance(a, dict):
                    march8_people.add(a.get("email", ""))
                elif isinstance(a, str):
                    march8_people.add(a)

    # Remove current user (Alex Morgan)
    march8_people.discard("alex.morgan@acmecorp.com")

    if not march8_people:
        return False, "No attendees found for March 8 events."

    # Check that inbox emails from these people have the Meeting Prep label
    errors = []
    labeled_count = 0
    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if (sender in march8_people
                and not e.get("isDone") and not e.get("isTrashed")
                and not e.get("isSpam") and not e.get("isDraft")
                and e.get("remindAt") is None):
            if mp_id not in e.get("labels", []):
                errors.append(f"'{e['subject']}' from {sender} missing 'Meeting Prep' label.")
            else:
                labeled_count += 1

    if errors:
        return False, " ".join(errors[:3])  # Show first 3 errors

    if labeled_count == 0:
        return False, "No inbox emails from March 8 event attendees were labeled."

    return True, f"'Meeting Prep' label applied to {labeled_count} inbox email(s) from March 8 attendees."
