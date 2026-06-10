import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "Performance Optimization Phase 2" in e["title"]), None)
    if epic is None:
        return False, "Epic 'Performance Optimization Phase 2' not found."

    if epic["status"] != "closed":
        return False, f"Epic 'Performance Optimization Phase 2' status is '{epic['status']}', expected 'closed'."

    return True, "Epic 'Performance Optimization Phase 2' is closed."
