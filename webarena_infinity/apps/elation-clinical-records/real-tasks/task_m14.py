import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    target_template = None
    for t in templates:
        if t.get("name") == "Pre-Operative Evaluation":
            target_template = t
            break

    if target_template is None:
        template_names = [t.get("name") for t in templates]
        return False, f"Could not find template named 'Pre-Operative Evaluation'. Current templates: {template_names}"

    expected_notes = "Pre-op clearance - ensure all required labs are completed prior to surgery."
    billing_notes = target_template.get("billingNotes", "")
    if billing_notes != expected_notes:
        return False, f"Pre-Operative Evaluation billingNotes is '{billing_notes}', expected '{expected_notes}'."

    return True, "Successfully verified that Pre-Operative Evaluation template billing notes were updated."
