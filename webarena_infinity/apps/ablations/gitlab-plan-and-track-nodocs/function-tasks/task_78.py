import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [e for e in state["epics"] if e["title"] == "Security Penetration Testing"]
    if not match:
        return False, "Epic 'Security Penetration Testing' not found."
    epic = match[0]
    if epic["confidential"] is not True:
        return False, f"Epic confidential is {epic['confidential']}, expected True."
    if epic["status"] != "open":
        return False, f"Epic status is '{epic['status']}', expected 'open'."
    return True, "Confidential epic 'Security Penetration Testing' created."
