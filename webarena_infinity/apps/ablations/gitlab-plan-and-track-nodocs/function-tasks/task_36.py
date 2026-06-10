import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ms = next((m for m in state["milestones"] if "v1.0" in m["title"]), None)
    if not ms:
        return False, "Milestone 'v1.0 — Foundation' not found."

    if ms["status"] != "active":
        return False, f"Milestone status is '{ms['status']}', expected 'active'."

    return True, "Milestone 'v1.0 — Foundation' reopened."
