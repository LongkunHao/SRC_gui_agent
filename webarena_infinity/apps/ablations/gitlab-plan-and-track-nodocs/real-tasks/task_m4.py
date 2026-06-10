import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if e["title"] == "Dark Mode Support"), None)
    if epic is None:
        return False, "Epic with title 'Dark Mode Support' not found."

    if 8 not in epic.get("labels", []):
        return False, f"Label 'frontend' (id 8) not in epic labels: {epic.get('labels', [])}."

    if 6 not in epic.get("labels", []):
        return False, f"Label 'UX' (id 6) not in epic labels: {epic.get('labels', [])}."

    if "dark mode" not in epic.get("description", "").lower():
        return False, f"Description does not contain 'dark mode'. Got: '{epic.get('description', '')}'."

    return True, "Epic 'Dark Mode Support' created with frontend and UX labels and correct description."
