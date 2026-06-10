# Task: Find most recently saved person in other contacts, move with specific fields.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Most recently saved person = Jason Blake (2026-02-10)
    # Should be moved to main contacts with company/title/label set
    contacts = state.get("contacts", [])
    jason = None
    for c in contacts:
        if c.get("email") == "jason.blake@salesforce.com":
            jason = c
            break

    if jason is None:
        errors.append("Jason Blake not found in main contacts")
    else:
        if jason.get("company") != "Salesforce":
            errors.append(
                f"Company is '{jason.get('company')}' instead of 'Salesforce'"
            )
        if jason.get("jobTitle") != "Account Executive":
            errors.append(
                f"Job title is '{jason.get('jobTitle')}' instead of 'Account Executive'"
            )
        if "clabel_3" not in jason.get("labels", []):
            errors.append("Jason Blake should have the Work label")

    # Should be removed from other contacts
    other_contacts = state.get("otherContacts", [])
    for oc in other_contacts:
        if oc.get("email") == "jason.blake@salesforce.com":
            errors.append("Jason Blake should be removed from other contacts")
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Jason Blake moved to main contacts with correct fields."
