# Task: Find earliest-activated delegate, update their contact's job title.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Laura Johnson-Martinez was activated earliest (2024-12-02 vs Maya's 2025-06-16)
    laura = None
    for c in contacts:
        if c.get("firstName") == "Laura" and c.get("lastName") == "Johnson-Martinez":
            laura = c
            break

    if laura is None:
        errors.append("Laura Johnson-Martinez not found")
    elif laura.get("jobTitle") != "Senior Marketing Director":
        errors.append(
            f"Laura Johnson-Martinez job title is '{laura.get('jobTitle')}' "
            "instead of 'Senior Marketing Director'"
        )

    if errors:
        return False, "; ".join(errors)
    return True, "Earliest-activated delegate's contact updated to Senior Marketing Director."
