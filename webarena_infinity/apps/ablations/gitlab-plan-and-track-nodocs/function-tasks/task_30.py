import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    label = next((l for l in state["labels"] if l["name"] == "tech-debt"), None)
    if not label:
        return False, "Label 'tech-debt' not found."

    expected = "Legacy code cleanup and refactoring"
    if label["description"] != expected:
        return False, f"Label description is '{label['description']}', expected '{expected}'."

    return True, "Label 'tech-debt' description updated."
