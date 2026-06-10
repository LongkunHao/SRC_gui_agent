import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Nate Patel (engineering): emails 7, 119 → should be archived
    # Maya Patel (design): emails 8, 114 → should be starred
    nate_emails = []
    maya_emails = []

    for e in state.get("emails", []):
        sender = e["from"]["email"]
        if sender == "nate.patel@acmecorp.com":
            # Check if this was an inbox email (Important split)
            if e.get("splitCategory") == "important":
                nate_emails.append(e)
        elif sender == "maya.patel@acmecorp.com":
            if e.get("splitCategory") == "important":
                maya_emails.append(e)

    errors = []

    # Check Nate's emails are archived
    for e in nate_emails:
        if not e.get("isDone"):
            errors.append(f"Nate Patel's '{e['subject']}' is not archived.")

    # Check Maya's emails are starred
    for e in maya_emails:
        if not e.get("isStarred"):
            errors.append(f"Maya Patel's '{e['subject']}' is not starred.")

    if errors:
        return False, " ".join(errors)

    if not nate_emails:
        return False, "No inbox emails found from Nate Patel."
    if not maya_emails:
        return False, "No inbox emails found from Maya Patel."

    return True, f"Nate Patel's emails archived ({len(nate_emails)}); Maya Patel's emails starred ({len(maya_emails)})."
