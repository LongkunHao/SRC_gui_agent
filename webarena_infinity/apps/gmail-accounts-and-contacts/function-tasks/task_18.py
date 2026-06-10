import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    labels = state.get("contactLabels", [])
    family_label = None
    for label in labels:
        if label.get("name") == "Family":
            family_label = label
            break

    if family_label is None:
        return False, "No label with name 'Family' found."

    if family_label.get("color") != "#34A853":
        return False, f"Family label color is '{family_label.get('color')}', expected '#34A853'."

    return True, "Family label has color '#34A853'."
