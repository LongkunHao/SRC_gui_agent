import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    target_template = None
    for t in templates:
        if t.get("name") == "Diabetes Management":
            target_template = t
            break

    if target_template is None:
        template_names = [t.get("name") for t in templates]
        return False, f"Could not find template named 'Diabetes Management'. Current templates: {template_names}"

    doc_tags = target_template.get("documentTags", [])
    if "Chronic-Pain" not in doc_tags:
        return False, f"Template 'Diabetes Management' documentTags does not include 'Chronic-Pain'. Current tags: {doc_tags}"

    return True, "Successfully verified that 'Chronic-Pain' tag was added to the Diabetes Management template."
