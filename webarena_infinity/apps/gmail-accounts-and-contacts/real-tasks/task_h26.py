# Task: Star all Neighbors, remove Neighbors label from those also in Book Club.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    contact_map = {}
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        contact_map[name] = c

    # All three Neighbors should be starred
    neighbors = ["Samantha Lee", "Ben Walker", "Tony Russo"]
    for name in neighbors:
        contact = contact_map.get(name)
        if contact is None:
            errors.append(f"Contact '{name}' not found")
            continue
        if not contact.get("isStarred"):
            errors.append(f"'{name}' (Neighbor) should be starred but is not")

    # Samantha Lee and Tony Russo are also in Book Club -> Neighbors label removed
    should_lose_neighbors = ["Samantha Lee", "Tony Russo"]
    for name in should_lose_neighbors:
        contact = contact_map.get(name)
        if contact and "clabel_7" in contact.get("labels", []):
            errors.append(
                f"'{name}' still has Neighbors label (should be removed, also in Book Club)"
            )

    # Ben Walker is NOT in Book Club -> should keep Neighbors
    ben = contact_map.get("Ben Walker")
    if ben and "clabel_7" not in ben.get("labels", []):
        errors.append("Ben Walker lost the Neighbors label but should have kept it")

    if errors:
        return False, "; ".join(errors)
    return True, "All Neighbors starred; Neighbors label removed from Book Club members."
