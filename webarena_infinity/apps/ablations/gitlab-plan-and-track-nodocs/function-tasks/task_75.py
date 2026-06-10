import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    ms = next((m for m in state["milestones"] if m["id"] == 4), None)
    if not ms:
        return False, "Milestone with id 4 not found."
    if ms["startDate"] != "2026-05-15":
        return False, f"Start date is '{ms['startDate']}', expected '2026-05-15'."
    if ms["dueDate"] != "2026-07-15":
        return False, f"Due date is '{ms['dueDate']}', expected '2026-07-15'."
    return True, "Milestone 'v2.1 \u2014 Integrations' dates updated."
