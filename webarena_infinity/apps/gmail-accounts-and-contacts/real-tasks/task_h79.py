# Task: Find contact with 'property search in East Bay' in notes, add as delegate, add VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Tom Bradley: notes mention "property search in East Bay"
    # Should be added as delegate and have VIP Clients label
    delegates = state.get("delegates", [])
    tom_delegate = None
    for d in delegates:
        if d.get("email") == "tom.bradley@realtyhome.com":
            tom_delegate = d
            break

    if tom_delegate is None:
        errors.append("Tom Bradley not found as a delegate")
    else:
        if tom_delegate.get("name") != "Tom Bradley":
            errors.append(
                f"Delegate name is '{tom_delegate.get('name')}' instead of 'Tom Bradley'"
            )

    contacts = state.get("contacts", [])
    tom_contact = None
    for c in contacts:
        if c.get("firstName") == "Tom" and c.get("lastName") == "Bradley":
            tom_contact = c
            break

    if tom_contact is None:
        errors.append("Tom Bradley contact not found")
    elif "clabel_4" not in tom_contact.get("labels", []):
        errors.append("Tom Bradley should have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Tom Bradley added as delegate and VIP Clients label added."
