# Task: Find Stanford contact, remove College Alumni, add Work and VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    robert = None
    for c in contacts:
        if c.get("firstName") == "Robert" and c.get("lastName") == "Singh":
            robert = c
            break

    if robert is None:
        errors.append("Robert Singh not found")
    else:
        if "clabel_6" in robert.get("labels", []):
            errors.append("Robert Singh should not have the College Alumni label")
        if "clabel_3" not in robert.get("labels", []):
            errors.append("Robert Singh should have the Work label")
        if "clabel_4" not in robert.get("labels", []):
            errors.append("Robert Singh should have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Robert Singh: College Alumni removed, Work and VIP Clients added."
