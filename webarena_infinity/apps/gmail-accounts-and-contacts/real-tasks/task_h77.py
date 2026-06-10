# Task: Create Hiro Tanaka contact, add same labels as Yuki Tanaka.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Yuki Tanaka has labels: clabel_2 (Friends), clabel_11 (Travel Contacts)
    yuki = None
    for c in contacts:
        if c.get("firstName") == "Yuki" and c.get("lastName") == "Tanaka":
            yuki = c
            break

    if yuki is None:
        errors.append("Yuki Tanaka not found")

    # Check Hiro Tanaka exists with correct email and labels
    hiro = None
    for c in contacts:
        if c.get("firstName") == "Hiro" and c.get("lastName") == "Tanaka":
            hiro = c
            break

    if hiro is None:
        errors.append("Hiro Tanaka not found in contacts")
    else:
        if hiro.get("email") != "hiro.tanaka@gmail.com":
            errors.append(
                f"Hiro's email is '{hiro.get('email')}' instead of 'hiro.tanaka@gmail.com'"
            )
        # Should have same labels as Yuki: Friends and Travel Contacts
        if "clabel_2" not in hiro.get("labels", []):
            errors.append("Hiro Tanaka should have the Friends label")
        if "clabel_11" not in hiro.get("labels", []):
            errors.append("Hiro Tanaka should have the Travel Contacts label")

    if errors:
        return False, "; ".join(errors)
    return True, "Hiro Tanaka created with Yuki Tanaka's labels."
