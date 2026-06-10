import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    labels = state.get("contactLabels", [])
    label_names = [label.get("name") for label in labels]
    if "Gym Buddies" in label_names:
        return False, "Label 'Gym Buddies' still exists but should have been renamed/deleted."
    if "Fitness Friends" not in label_names:
        return False, "Label 'Fitness Friends' does not exist."
    return True, "Label 'Gym Buddies' does not exist and label 'Fitness Friends' exists."
