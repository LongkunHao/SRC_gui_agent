import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check that no label with name "Receipts" exists
    for label in state.get("labels", []):
        if label.get("name") == "Receipts":
            return False, "Label 'Receipts' still exists in state. It should have been deleted."

    return True, "Label 'Receipts' has been successfully deleted."
