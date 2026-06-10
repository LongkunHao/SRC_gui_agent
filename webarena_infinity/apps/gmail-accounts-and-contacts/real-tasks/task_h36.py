# Task: Replace Healthcare label with Emergency, then delete Healthcare label.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    contact_labels = state.get("contactLabels", [])

    # Healthcare label (clabel_12) should be deleted
    for lbl in contact_labels:
        if lbl.get("id") == "clabel_12" or lbl.get("name") == "Healthcare":
            errors.append("Healthcare label still exists")

    # No contact should reference clabel_12
    for c in contacts:
        if "clabel_12" in c.get("labels", []):
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            errors.append(f"Contact '{name}' still has Healthcare label reference")

    # Contacts that had Healthcare should now have Emergency (clabel_10):
    # Dr. Patricia Nguyen (already had Emergency), Mike Chen, Hannah Brooks, Diana Castillo
    should_have_emergency = [
        ("Dr. Patricia", "Nguyen"),
        ("Mike", "Chen"),
        ("Hannah", "Brooks"),
        ("Diana", "Castillo"),
    ]

    for first, last in should_have_emergency:
        contact = None
        for c in contacts:
            if c.get("firstName") == first and c.get("lastName") == last:
                contact = c
                break
        if contact is None:
            # Contact might not exist (shouldn't be deleted by this task)
            errors.append(f"{first} {last} not found")
            continue
        if "clabel_10" not in contact.get("labels", []):
            errors.append(
                f"{first} {last} should have Emergency label (replaced Healthcare)"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Healthcare label replaced with Emergency and deleted."
