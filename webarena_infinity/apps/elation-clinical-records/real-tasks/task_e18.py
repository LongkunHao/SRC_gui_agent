import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    found = False
    for t in templates:
        if t.get("name") == "Diabetes Management (Copy)":
            found = True
            break

    if not found:
        template_names = [t.get("name") for t in templates]
        return False, f"Template 'Diabetes Management (Copy)' not found. Existing templates: {template_names}"

    return True, "Successfully verified that 'Diabetes Management (Copy)' template exists (duplication successful)."
