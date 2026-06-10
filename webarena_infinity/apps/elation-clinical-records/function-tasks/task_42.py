import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    expected_hpi = (
        "Patient returns for blood pressure management follow-up. "
        "Reviewing home BP log and medication compliance."
    )

    templates = state.get("visitNoteTemplates", [])
    for tmpl in templates:
        if tmpl.get("name") == "Hypertension Follow-Up" or tmpl.get("id") == "tmpl_007":
            content = tmpl.get("content", {})
            hpi = content.get("hpi", "")
            if hpi == expected_hpi:
                return True, "Template 'Hypertension Follow-Up' has the expected HPI content."
            return False, f"Template 'Hypertension Follow-Up' found but content.hpi is '{hpi}', expected '{expected_hpi}'."

    return False, "Template 'Hypertension Follow-Up' (tmpl_007) not found."
