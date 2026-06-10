import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "Accessibility Compliance" in e["title"]), None)
    if epic is None:
        return False, "Epic 'Accessibility Compliance (WCAG 2.1 AA)' not found."

    if epic["status"] != "closed":
        return False, f"Epic 'Accessibility Compliance' status is '{epic['status']}', expected 'closed'."

    return True, "Epic 'Accessibility Compliance (WCAG 2.1 AA)' is closed."
