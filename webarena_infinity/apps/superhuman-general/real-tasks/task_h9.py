import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Find "Re: Infrastructure Migration Plan" from "Tom Bradley" → isDone==true
    tom_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Re: Infrastructure Migration Plan" and e["from"]["name"] == "Tom Bradley":
            tom_email = e
            break
    if not tom_email:
        errors.append("Could not find 'Re: Infrastructure Migration Plan' from Tom Bradley.")
    elif not tom_email.get("isDone", False):
        errors.append("Tom Bradley's migration email is not archived (isDone is not true).")

    # Find "Logistics Update - Office Equipment Delivery" from "Carlos Mendez" → isDone==true
    carlos_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Logistics Update - Office Equipment Delivery" and e["from"]["name"] == "Carlos Mendez":
            carlos_email = e
            break
    if not carlos_email:
        errors.append("Could not find 'Logistics Update - Office Equipment Delivery' from Carlos Mendez.")
    elif not carlos_email.get("isDone", False):
        errors.append("Carlos Mendez's logistics email is not archived (isDone is not true).")

    # Find "CloudScale Contract - Ready to Sign" from "Michael Foster" → isStarred==true
    michael_email = None
    for e in state.get("emails", []):
        if e["subject"] == "CloudScale Contract - Ready to Sign" and e["from"]["name"] == "Michael Foster":
            michael_email = e
            break
    if not michael_email:
        errors.append("Could not find 'CloudScale Contract - Ready to Sign' from Michael Foster.")
    elif not michael_email.get("isStarred", False):
        errors.append("Michael Foster's CloudScale contract email is not starred.")

    if errors:
        return False, " | ".join(errors)

    return True, "Tom's and Carlos's emails archived, CloudScale contract email starred."
