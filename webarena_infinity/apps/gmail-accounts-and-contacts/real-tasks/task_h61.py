# Task: Find contact with 'vendor agreements and NDAs' in notes, change company, add VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    james = None
    for c in contacts:
        if c.get("firstName") == "James" and c.get("lastName") == "O'Brien":
            james = c
            break

    if james is None:
        errors.append("James O'Brien not found")
    else:
        if james.get("company") != "Morrison Legal Group":
            errors.append(
                f"Company is '{james.get('company')}' instead of 'Morrison Legal Group'"
            )
        if "clabel_4" not in james.get("labels", []):
            errors.append("James O'Brien does not have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "James O'Brien company updated and VIP Clients label added."
