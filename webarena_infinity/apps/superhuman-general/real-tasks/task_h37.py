import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Work label
    work_label = None
    for label in state.get("labels", []):
        if label["name"] == "Work":
            work_label = label
            break
    if not work_label:
        return False, "Label 'Work' not found."
    work_id = work_label["id"]

    # Find Sarah Chen's customer escalation email
    escalation = None
    for e in state.get("emails", []):
        if (e["subject"] == "Customer Escalation - Enterprise Client"
                and e["from"]["email"] == "sarah.chen@acmecorp.com"):
            escalation = e
            break
    if not escalation:
        return False, "Could not find 'Customer Escalation - Enterprise Client' from Sarah Chen."

    errors = []
    if escalation.get("isDone", False):
        errors.append("Email is still in Done (isDone=true); should be moved back to inbox.")
    if work_id not in escalation.get("labels", []):
        errors.append(f"Email does not have the 'Work' label (labels: {escalation.get('labels', [])}).")

    if errors:
        return False, " ".join(errors)

    return True, "Customer escalation email moved from Done to inbox with 'Work' label added."
