import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    for tmpl in templates:
        if tmpl.get("name") == "Diabetes Management" or tmpl.get("id") == "tmpl_006":
            tags = tmpl.get("documentTags", [])
            if "Chronic-Pain" in tags:
                return True, "Template 'Diabetes Management' has 'Chronic-Pain' in documentTags."
            return False, f"Template 'Diabetes Management' found but documentTags is {tags}, missing 'Chronic-Pain'."

    return False, "Template 'Diabetes Management' (tmpl_006) not found."
