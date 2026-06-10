# Task: Find contact with 'AWS re:Invent 2024' in notes, add College Alumni, update address.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Sarah Chen: notes mention "AWS re:Invent 2024"
    contacts = state.get("contacts", [])
    sarah = None
    for c in contacts:
        if c.get("firstName") == "Sarah" and c.get("lastName") == "Chen":
            sarah = c
            break

    if sarah is None:
        errors.append("Sarah Chen not found")
    else:
        if "clabel_6" not in sarah.get("labels", []):
            errors.append("Sarah Chen should have the College Alumni label")
        if sarah.get("address") != "500 Tech Park Dr, Menlo Park, CA 94025":
            errors.append(
                f"Address is '{sarah.get('address')}' instead of "
                f"'500 Tech Park Dr, Menlo Park, CA 94025'"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Sarah Chen: College Alumni added and address updated."
