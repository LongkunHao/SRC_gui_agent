import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    label = next((l for l in state["labels"] if l["name"] == "bug"), None)
    if not label:
        return False, "Label 'bug' not found."

    if label["color"].lower() != "#ff0000":
        return False, f"Label color is '{label['color']}', expected '#ff0000'."

    return True, "Label 'bug' color changed to '#ff0000'."
