import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ms = next((m for m in state["milestones"] if m["title"] == "v3.1 — Analytics"), None)
    if not ms:
        # Also try without em-dash
        ms = next((m for m in state["milestones"] if "v3.1" in m["title"] and "Analytics" in m["title"]), None)
    if not ms:
        return False, "Milestone 'v3.1 — Analytics' not found."

    if ms["startDate"] != "2026-11-01":
        return False, f"Start date is '{ms['startDate']}', expected '2026-11-01'."

    if ms["dueDate"] != "2027-01-31":
        return False, f"Due date is '{ms['dueDate']}', expected '2027-01-31'."

    return True, "Milestone 'v3.1 — Analytics' created with correct dates."
