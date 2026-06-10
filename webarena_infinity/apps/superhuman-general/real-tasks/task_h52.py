import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    work_label = None
    for label in state.get("labels", []):
        if label["name"] == "Work":
            work_label = label
            break
    if not work_label:
        return False, "Label 'Work' not found."

    email = None
    for e in state.get("emails", []):
        if (e["subject"] == "Consulting Engagement Summary"
                and e["from"]["email"] == "omar.ar@consulting.group"):
            email = e
            break
    if not email:
        return False, "Could not find 'Consulting Engagement Summary' email from Omar Al-Rashid."

    errors = []
    if email.get("isDone"):
        errors.append("Email is still in Done (isDone=true); should be moved back to inbox.")
    if work_label["id"] not in email.get("labels", []):
        errors.append(f"Email does not have the 'Work' label (labels: {email.get('labels', [])}).")
    if not email.get("remindAt"):
        errors.append("No reminder set on the email.")
    else:
        remind = email["remindAt"]
        if "2026-03-10" not in remind:
            errors.append(f"Reminder is set for '{remind}', expected March 10.")

    if errors:
        return False, " ".join(errors)

    return True, "Consulting engagement email moved from Done, Work label added, reminder set for March 10."
