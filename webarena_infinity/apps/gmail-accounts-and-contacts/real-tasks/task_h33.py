# Task: Move all auto-saved contacts with @techcorp.io email to main contacts.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    other_contacts = state.get("otherContacts", [])

    # Two auto-saved contacts have @techcorp.io:
    # hr@techcorp.io (TechCorp HR) and wendy.chung@techcorp.io (Wendy Chung)
    techcorp_emails = ["hr@techcorp.io", "wendy.chung@techcorp.io"]

    for email in techcorp_emails:
        # Should be in main contacts
        in_main = any(c.get("email") == email for c in contacts)
        if not in_main:
            errors.append(f"'{email}' not found in main contacts after move")

        # Should not be in other contacts
        in_other = any(c.get("email") == email for c in other_contacts)
        if in_other:
            errors.append(f"'{email}' still in other contacts after move")

    if errors:
        return False, "; ".join(errors)
    return True, "All @techcorp.io auto-saved contacts moved to main contacts."
