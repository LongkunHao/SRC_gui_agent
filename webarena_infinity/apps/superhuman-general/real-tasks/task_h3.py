import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find "Follow Up" label
    follow_up_label = None
    for label in state.get("labels", []):
        if label["name"] == "Follow Up":
            follow_up_label = label
            break
    if not follow_up_label:
        return False, "Label 'Follow Up' not found in labels."
    if follow_up_label.get("type") != "user":
        return False, f"Label 'Follow Up' has type '{follow_up_label.get('type')}' instead of 'user'."
    follow_up_id = follow_up_label["id"]

    # Find James O'Brien's vendor agreement email
    vendor_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Re: Vendor Agreement - CloudScale" and e["from"]["name"] == "James O'Brien":
            vendor_email = e
            break
    if not vendor_email:
        return False, "Could not find 'Re: Vendor Agreement - CloudScale' email from James O'Brien."

    # Find Jennifer Wu's research proposal email
    research_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Research Collaboration Proposal" and e["from"]["name"] == "Jennifer Wu":
            research_email = e
            break
    if not research_email:
        return False, "Could not find 'Research Collaboration Proposal' email from Jennifer Wu."

    # Check both emails have the Follow Up label
    if follow_up_id not in vendor_email.get("labels", []):
        return False, f"Vendor Agreement email does not have 'Follow Up' label (expected '{follow_up_id}' in {vendor_email.get('labels', [])})."
    if follow_up_id not in research_email.get("labels", []):
        return False, f"Research Proposal email does not have 'Follow Up' label (expected '{follow_up_id}' in {research_email.get('labels', [])})."

    return True, "Label 'Follow Up' created and applied to both emails."
