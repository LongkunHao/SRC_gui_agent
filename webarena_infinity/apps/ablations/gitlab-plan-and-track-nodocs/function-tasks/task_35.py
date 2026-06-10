import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ms = next((m for m in state["milestones"] if "v2.0" in m["title"]), None)
    if not ms:
        return False, "Milestone 'v2.0 — API Overhaul' not found."

    if ms["status"] != "closed":
        return False, f"Milestone status is '{ms['status']}', expected 'closed'."

    return True, "Milestone 'v2.0 — API Overhaul' closed."
