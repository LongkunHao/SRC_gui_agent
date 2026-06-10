import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # All-Hands Meeting organizer is patrick.oneil@acmecorp.com
    # Patrick's inbox email: "Executive Team Dinner - March 14"
    # Add Finance label

    finance_label = None
    for label in state.get("labels", []):
        if label["name"] == "Finance":
            finance_label = label
            break
    if not finance_label:
        return False, "Label 'Finance' not found."

    email = None
    for e in state.get("emails", []):
        if (e["subject"] == "Executive Team Dinner - March 14"
                and e["from"]["email"] == "patrick.oneil@acmecorp.com"):
            email = e
            break
    if not email:
        return False, "Could not find 'Executive Team Dinner - March 14' email from Patrick O'Neil."

    if finance_label["id"] not in email.get("labels", []):
        return False, f"Email does not have the 'Finance' label (labels: {email.get('labels', [])})."

    return True, "Finance label added to Patrick O'Neil's email (discovered via All-Hands organizer)."
