import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    if state["preferences"]["gitAttachmentFormat"] == "Title and repository":
        return True, "Git attachment format correctly set to 'Title and repository'."
    return False, f"Expected gitAttachmentFormat to be 'Title and repository', got '{state['preferences']['gitAttachmentFormat']}'."
