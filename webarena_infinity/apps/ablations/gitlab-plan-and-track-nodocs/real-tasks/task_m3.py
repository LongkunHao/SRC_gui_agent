import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    milestone = next((m for m in state["milestones"] if "v2.2" in m["title"]), None)
    if milestone is None:
        return False, "No milestone with 'v2.2' in the title found."

    if milestone.get("startDate") != "2026-07-01":
        return False, f"startDate is '{milestone.get('startDate')}', expected '2026-07-01'."

    if milestone.get("dueDate") != "2026-08-31":
        return False, f"dueDate is '{milestone.get('dueDate')}', expected '2026-08-31'."

    if "Performance improvements" not in milestone.get("description", ""):
        return False, f"Description does not contain 'Performance improvements'. Got: '{milestone.get('description', '')}'."

    return True, "Milestone 'v2.2 — Performance' created with correct dates and description."
