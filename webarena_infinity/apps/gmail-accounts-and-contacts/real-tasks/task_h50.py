# Task: Add Emergency label to all delegate contacts, remove non-active delegates.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    delegates = state.get("delegates", [])

    # All contacts who were delegates should have Emergency label (clabel_10)
    delegate_contacts = [
        ("Maya", "Patel"),              # delegate_1, active
        ("Laura", "Johnson-Martinez"),  # delegate_2, active
        ("Priya", "Sharma"),            # delegate_3, pending
        ("Jake", "Morrison"),           # delegate_4, expired
    ]

    for first, last in delegate_contacts:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
            continue
        if "clabel_10" not in contact.get("labels", []):
            errors.append(f"{first} {last} should have Emergency label (is a delegate)")

    # Only active delegates should remain
    for d in delegates:
        if d.get("status") != "active":
            errors.append(
                f"Delegate '{d.get('email')}' with status '{d.get('status')}' "
                "should have been removed (not active)"
            )

    # Active delegates should still exist
    active_emails = {"maya.patel@techcorp.io", "laura.jm@gmail.com"}
    for email in active_emails:
        found = any(d.get("email") == email for d in delegates)
        if not found:
            errors.append(f"Active delegate '{email}' should still exist")

    if errors:
        return False, "; ".join(errors)
    return True, "Emergency label added to delegate contacts, non-active delegates removed."
