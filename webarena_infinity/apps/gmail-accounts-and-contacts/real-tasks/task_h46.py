# Task: Star every contact whose only label is Work.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Contacts with exactly [Work] as their only label should be starred
    work_only_names = [
        ("Priya", "Sharma"),
        ("Lisa", "Nakamura"),
        ("Michelle", "Park"),
        ("Nate", "Patel"),
        ("Omar", "Al-Rashid"),
        ("Jennifer", "Wu"),
        ("Maya", "Patel"),
        ("Aisha", "Mohammed"),
        ("Raj", "Kapoor"),
        ("Patricia", "Wong-Anderson"),
    ]

    for first, last in work_only_names:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            errors.append(f"{first} {last} not found")
            continue
        if not contact.get("isStarred"):
            errors.append(f"{first} {last} should be starred (only label is Work)")

    if errors:
        return False, "; ".join(errors)
    return True, "All contacts with Work as their only label are starred."
