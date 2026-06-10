import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    labels = state.get("labels", state.get("contactLabels", []))
    label_names = [l.get("name", "") for l in labels if isinstance(l, dict)]
    college_alumni_exists = "College Alumni" in label_names
    university_network_exists = "University Network" in label_names
    if college_alumni_exists:
        return False, "Label 'College Alumni' still exists but should have been renamed/removed."
    if not university_network_exists:
        return False, f"Label 'University Network' not found. Existing labels: {label_names}"
    return True, "Label 'College Alumni' does not exist and label 'University Network' exists."
