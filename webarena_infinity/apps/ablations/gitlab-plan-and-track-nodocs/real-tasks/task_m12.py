import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    label = next((l for l in state["labels"] if l["name"] == "security"), None)
    if label is None:
        return False, "Label with name 'security' not found."

    if label.get("color", "").lower() != "#8e44ad":
        return False, f"Label color is '{label.get('color')}', expected '#8e44ad'."

    if label.get("description") != "Security vulnerabilities and hardening":
        return False, f"Label description is '{label.get('description')}', expected 'Security vulnerabilities and hardening'."

    return True, "Security label updated with color '#8e44ad' and description 'Security vulnerabilities and hardening'."
