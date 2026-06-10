import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ms = next((m for m in state["milestones"] if m["title"] == "Backlog"), None)
    if not ms:
        return False, "Milestone 'Backlog' not found."

    expected = "Unscheduled items awaiting prioritization"
    if ms["description"] != expected:
        return False, f"Description is '{ms['description']}', expected '{expected}'."

    return True, "Milestone 'Backlog' description updated."
