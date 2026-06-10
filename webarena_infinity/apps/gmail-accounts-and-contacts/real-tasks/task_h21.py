# Task: Remove any delegate whose corresponding contact entry has the Work label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    delegates = state.get("delegates", [])
    contacts = state.get("contacts", [])

    # Build lookup: email -> contact labels
    contact_labels_by_email = {}
    for c in contacts:
        contact_labels_by_email[c.get("email", "")] = c.get("labels", [])

    # Maya Patel (maya.patel@techcorp.io) has Work label -> should be removed
    # Priya Sharma (priya.sharma@cloudnine.dev) has Work label -> should be removed
    should_be_removed = {"maya.patel@techcorp.io", "priya.sharma@cloudnine.dev"}
    should_remain = {"laura.jm@gmail.com", "jake.morrison@gmail.com"}

    for email in should_be_removed:
        for d in delegates:
            if d.get("email") == email:
                errors.append(
                    f"Delegate '{email}' should have been removed (contact has Work label)"
                )

    for email in should_remain:
        found = any(d.get("email") == email for d in delegates)
        if not found:
            errors.append(
                f"Delegate '{email}' should still exist (contact does not have Work label)"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "All delegates with Work-labeled contacts removed successfully."
