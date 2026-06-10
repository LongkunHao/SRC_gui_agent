import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    target_template = None
    for t in templates:
        if t.get("name") == "Chronic Pain Follow-Up":
            target_template = t
            break

    if target_template is None:
        template_names = [t.get("name") for t in templates]
        return False, f"Could not find template named 'Chronic Pain Follow-Up'. Current templates: {template_names}"

    content = target_template.get("content", {})
    hpi = content.get("hpi", "")
    if not hpi:
        return False, f"Template 'Chronic Pain Follow-Up' has no HPI content. Content keys: {list(content.keys())}"

    return True, "Successfully verified that template 'Chronic Pain Follow-Up' was created with an HPI section."
