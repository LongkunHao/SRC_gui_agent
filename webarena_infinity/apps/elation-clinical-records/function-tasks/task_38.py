import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    for tmpl in templates:
        name = tmpl.get("name", "")
        if "Annual Wellness Visit (Copy)" in name:
            return True, f"Found duplicated template: '{name}'."

    return False, "No template matching '*Annual Wellness Visit (Copy)' found in visitNoteTemplates."
