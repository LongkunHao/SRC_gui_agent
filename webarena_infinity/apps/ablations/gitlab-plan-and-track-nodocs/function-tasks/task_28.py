import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    label = next((l for l in state["labels"] if l["name"] == "infrastructure"), None)
    if not label:
        return False, "Label 'infrastructure' not found."

    if label["color"].lower() != "#2ecc71":
        return False, f"Label color is '{label['color']}', expected '#2ecc71'."

    return True, "Label 'infrastructure' created with color '#2ecc71'."
