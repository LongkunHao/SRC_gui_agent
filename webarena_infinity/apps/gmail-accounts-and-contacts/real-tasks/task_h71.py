# Task: Find contact with secondary email at @cs.stanford.edu, update title, add VIP Clients.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Robert Singh has secondary email r.singh@cs.stanford.edu
    contacts = state.get("contacts", [])
    robert = None
    for c in contacts:
        if c.get("firstName") == "Robert" and c.get("lastName") == "Singh":
            robert = c
            break

    if robert is None:
        errors.append("Robert Singh not found")
    else:
        if robert.get("jobTitle") != "Distinguished Professor":
            errors.append(
                f"Job title is '{robert.get('jobTitle')}' instead of 'Distinguished Professor'"
            )
        if "clabel_4" not in robert.get("labels", []):
            errors.append("Robert Singh should have the VIP Clients label")

    if errors:
        return False, "; ".join(errors)
    return True, "Robert Singh title updated and VIP Clients label added."
