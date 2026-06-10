import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    expected_billing_notes = "Pre-op clearance - ensure all required labs are completed prior to surgery."

    templates = state.get("visitNoteTemplates", [])
    for tmpl in templates:
        if tmpl.get("name") == "Pre-Operative Evaluation" or tmpl.get("id") == "tmpl_010":
            billing_notes = tmpl.get("billingNotes", "")
            if billing_notes == expected_billing_notes:
                return True, "Template 'Pre-Operative Evaluation' has the expected billingNotes."
            return False, f"Template 'Pre-Operative Evaluation' found but billingNotes is '{billing_notes}', expected '{expected_billing_notes}'."

    return False, "Template 'Pre-Operative Evaluation' (tmpl_010) not found."
