import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    label = next((l for l in state["labels"] if l["id"] == 10), None)
    if not label:
        return False, "Label with id 10 not found."
    if label["name"] != "technical-debt":
        return False, f"Label name is '{label['name']}', expected 'technical-debt'."
    return True, "Label renamed from 'tech-debt' to 'technical-debt'."
