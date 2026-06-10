# Task: Find the contact whose birthday is on March 8 and add the Emergency label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Emily Rodriguez has birthday 1985-03-08
    emily = None
    for c in contacts:
        if c.get("firstName") == "Emily" and c.get("lastName") == "Rodriguez":
            emily = c
            break

    if emily is None:
        errors.append("Emily Rodriguez not found in contacts")
    else:
        labels = emily.get("labels", [])
        # Emergency label is clabel_10
        if "clabel_10" not in labels:
            errors.append(
                "Emily Rodriguez (born March 8) does not have the Emergency label"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Emergency label added to the contact born on March 8 (Emily Rodriguez)."
