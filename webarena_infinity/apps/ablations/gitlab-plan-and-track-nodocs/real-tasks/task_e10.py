import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    milestone = next((m for m in state["milestones"] if "v1.1" in m["title"]), None)
    if milestone is None:
        return False, "Milestone 'v1.1 — Stability' not found."

    if milestone["status"] != "active":
        return False, f"Milestone 'v1.1' status is '{milestone['status']}', expected 'active'."

    return True, "Milestone 'v1.1 — Stability' is reopened (status is active)."
