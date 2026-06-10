import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    ms = next((m for m in state["milestones"] if m["id"] == 6), None)
    if not ms:
        return False, "Milestone with id 6 not found."
    if ms["title"] != "Product Backlog":
        return False, f"Title is '{ms['title']}', expected 'Product Backlog'."
    return True, "Milestone renamed from 'Backlog' to 'Product Backlog'."
