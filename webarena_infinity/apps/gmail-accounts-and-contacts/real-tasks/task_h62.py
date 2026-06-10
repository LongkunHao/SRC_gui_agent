# Task: Find most recently added delegate, update their contact job title.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Most recently added delegate is Priya Sharma (2026-03-05)
    contacts = state.get("contacts", [])
    priya = None
    for c in contacts:
        if c.get("firstName") == "Priya" and c.get("lastName") == "Sharma":
            priya = c
            break

    if priya is None:
        errors.append("Priya Sharma not found")
    else:
        if priya.get("jobTitle") != "Principal Engineer":
            errors.append(
                f"Job title is '{priya.get('jobTitle')}' instead of 'Principal Engineer'"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Most recently added delegate's contact updated to Principal Engineer."
