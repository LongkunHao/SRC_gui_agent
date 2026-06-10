# Task: Unstar contacts with exactly 1 label, star contacts with 3+ labels.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Contacts with exactly 1 label who were starred in seed:
    # Priya Sharma (clabel_3, starred), Maya Patel (clabel_3, starred),
    # Laura Johnson-Martinez (clabel_1, starred) -> all should be unstarred
    should_unstar = [
        ("Priya", "Sharma"),
        ("Maya", "Patel"),
        ("Laura", "Johnson-Martinez"),
    ]
    for first, last in should_unstar:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
        elif contact.get("isStarred"):
            errors.append(f"{first} {last} should be unstarred (has exactly 1 label)")

    # Contacts with 3+ labels who were not starred in seed:
    # Chris Evans (3 labels, not starred), Samantha Lee (3 labels, not starred)
    # -> should be starred
    should_star = [
        ("Chris", "Evans"),
        ("Samantha", "Lee"),
    ]
    for first, last in should_star:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
        elif not contact.get("isStarred"):
            errors.append(f"{first} {last} should be starred (has 3+ labels)")

    # Jake Morrison has 3 labels and is already starred -> should remain starred
    jake = None
    for c in contacts:
        if c.get("firstName") == "Jake" and c.get("lastName") == "Morrison":
            jake = c
            break
    if jake is not None and not jake.get("isStarred"):
        errors.append("Jake Morrison should remain starred (has 3 labels)")

    if errors:
        return False, "; ".join(errors)
    return True, "Contacts with 1 label unstarred, contacts with 3+ labels starred."
