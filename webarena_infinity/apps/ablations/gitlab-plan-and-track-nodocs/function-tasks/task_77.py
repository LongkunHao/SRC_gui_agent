import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [e for e in state["epics"] if e["title"] == "Documentation Overhaul"]
    if not match:
        return False, "Epic 'Documentation Overhaul' not found."
    epic = match[0]
    if epic["startDate"] != "2026-06-01":
        return False, f"Start date is '{epic['startDate']}', expected '2026-06-01'."
    if epic["dueDate"] != "2026-08-31":
        return False, f"Due date is '{epic['dueDate']}', expected '2026-08-31'."
    if epic["status"] != "open":
        return False, f"Status is '{epic['status']}', expected 'open'."
    return True, "Epic 'Documentation Overhaul' created with correct dates."
