import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Urgent" label and get its id
    urgent_label = None
    for label in state.get("labels", []):
        if label.get("name") == "Urgent":
            urgent_label = label
            break
    if not urgent_label:
        return False, "Could not find label 'Urgent' in state."
    urgent_id = urgent_label["id"]

    # Find the email "Q2 Product Roadmap - Final Review" from "Sarah Chen"
    target_email = None
    for e in state.get("emails", []):
        if (e.get("subject") == "Q2 Product Roadmap - Final Review"
                and e.get("from", {}).get("name") == "Sarah Chen"):
            target_email = e
            break
    if not target_email:
        return False, "Could not find email 'Q2 Product Roadmap - Final Review' from Sarah Chen."

    # Check that the Urgent label id is in the email's labels
    if urgent_id in target_email.get("labels", []):
        return True, "Urgent label has been successfully added to Sarah Chen's roadmap email."
    else:
        return False, f"Urgent label (id: {urgent_id}) not found in email labels: {target_email.get('labels', [])}."
