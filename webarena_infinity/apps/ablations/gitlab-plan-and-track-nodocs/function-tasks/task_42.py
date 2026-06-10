import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    epic = next((e for e in state["epics"] if e["title"] == "Data Export & Reporting"), None)
    if not epic:
        return False, "Epic 'Data Export & Reporting' not found."

    if epic["status"] != "open":
        return False, f"Epic status is '{epic['status']}', expected 'open'."

    return True, "Epic 'Data Export & Reporting' reopened."
