import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e["title"] == "Security Vulnerability Assessment"), None)
    if epic is None:
        return False, "Epic with title 'Security Vulnerability Assessment' not found."

    if epic.get("confidential") is not True:
        return False, f"Epic confidential is {epic.get('confidential')}, expected True."

    if 5 not in epic.get("labels", []):
        return False, f"Label 'security' (id 5) not in epic labels: {epic.get('labels', [])}."

    if 11 not in epic.get("labels", []):
        return False, f"Label 'priority::critical' (id 11) not in epic labels: {epic.get('labels', [])}."

    return True, "Confidential epic 'Security Vulnerability Assessment' created with security and priority::critical labels."
