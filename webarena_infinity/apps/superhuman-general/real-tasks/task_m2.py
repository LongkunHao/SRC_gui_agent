import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Marketing" label and get its id
    marketing_label = None
    for label in state.get("labels", []):
        if label.get("name") == "Marketing":
            marketing_label = label
            break
    if not marketing_label:
        return False, "Could not find label 'Marketing' in state."
    marketing_id = marketing_label["id"]

    # Find the email "New Brand Assets - Review Needed" from "Marcus Williams"
    target_email = None
    for e in state.get("emails", []):
        if (e.get("subject") == "New Brand Assets - Review Needed"
                and e.get("from", {}).get("name") == "Marcus Williams"):
            target_email = e
            break
    if not target_email:
        return False, "Could not find email 'New Brand Assets - Review Needed' from Marcus Williams."

    # Check that the Marketing label id is NOT in the email's labels
    if marketing_id not in target_email.get("labels", []):
        return True, "Marketing label has been successfully removed from Marcus Williams' brand assets email."
    else:
        return False, f"Marketing label (id: {marketing_id}) is still present in email labels: {target_email.get('labels', [])}."
