import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find label with name "Partnerships"
    partnerships_label = None
    for label in state.get("labels", []):
        if label.get("name") == "Partnerships":
            partnerships_label = label
            break

    if not partnerships_label:
        return False, "Could not find a label named 'Partnerships' in state."

    # Check it has type "user"
    if partnerships_label.get("type") != "user":
        return False, f"Label 'Partnerships' exists but has type '{partnerships_label.get('type')}' instead of 'user'."

    # Check color is set (not null/empty)
    color = partnerships_label.get("color")
    if not color:
        return False, "Label 'Partnerships' exists but has no color set."

    return True, f"Label 'Partnerships' has been created with type 'user' and color '{color}'."
