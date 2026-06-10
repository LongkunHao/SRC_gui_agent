import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    for tmpl in templates:
        if tmpl.get("name") == "Chronic Pain Follow-Up":
            content = tmpl.get("content", {})
            hpi = content.get("hpi", "")
            if "chronic pain management" in hpi.lower():
                return True, "Found template 'Chronic Pain Follow-Up' with HPI containing 'chronic pain management'."
            return False, f"Template 'Chronic Pain Follow-Up' found but HPI does not contain 'chronic pain management'. HPI: '{hpi}'."

    return False, "No template with name 'Chronic Pain Follow-Up' found."
