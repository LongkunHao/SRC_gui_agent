import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    templates = state.get("visitNoteTemplates", [])
    for t in templates:
        if t.get("name") == "Injectable Administration":
            return False, "Template 'Injectable Administration' still exists in visitNoteTemplates."

    return True, "Successfully verified that 'Injectable Administration' template has been deleted."
