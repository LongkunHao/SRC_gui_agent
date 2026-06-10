import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    label = next((l for l in state["labels"] if l["name"] == "env::production"), None)
    if not label:
        return False, "Label 'env::production' not found."

    if label.get("scoped") is not True:
        return False, f"Label scoped is {label.get('scoped')}, expected True."

    if label["color"].lower() != "#e74c3c":
        return False, f"Label color is '{label['color']}', expected '#e74c3c'."

    return True, "Scoped label 'env::production' created with color '#e74c3c'."
