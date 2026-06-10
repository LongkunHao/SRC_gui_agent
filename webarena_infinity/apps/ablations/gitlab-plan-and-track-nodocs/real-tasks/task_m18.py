import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    milestone = next((m for m in state["milestones"] if m["title"] == "Backlog"), None)
    if milestone is None:
        return False, "Milestone with title 'Backlog' not found."

    if milestone.get("description") != "Items not yet scheduled for a release":
        return False, f"Description is '{milestone.get('description')}', expected 'Items not yet scheduled for a release'."

    if milestone.get("startDate") != "2026-01-01":
        return False, f"startDate is '{milestone.get('startDate')}', expected '2026-01-01'."

    return True, "Backlog milestone updated with correct description and start date."
