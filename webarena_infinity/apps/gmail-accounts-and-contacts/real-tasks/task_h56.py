# Task: Unstar Friends contacts, then star unstarred VIP Clients contacts.
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

    # Friends contacts who were starred should now be unstarred
    friends_were_starred = ["Marcus Williams", "Jake Morrison"]
    for name in friends_were_starred:
        c = contact_map.get(name)
        if c is None:
            errors.append(f"{name} not found")
            continue
        if c.get("isStarred"):
            errors.append(f"{name} should be unstarred (has Friends label)")

    # VIP Clients who were not starred should now be starred
    vip_need_star = ["David Kim", "Ryan Cooper"]
    for name in vip_need_star:
        c = contact_map.get(name)
        if c is None:
            errors.append(f"{name} not found")
            continue
        if not c.get("isStarred"):
            errors.append(f"{name} should be starred (has VIP Clients)")

    # VIP Clients who were already starred should remain starred
    vip_already_starred = ["Sarah Chen", "Emily Rodriguez"]
    for name in vip_already_starred:
        c = contact_map.get(name)
        if c is None:
            errors.append(f"{name} not found")
            continue
        if not c.get("isStarred"):
            errors.append(f"{name} should still be starred (VIP Clients)")

    if errors:
        return False, "; ".join(errors)
    return True, "Friends contacts unstarred, VIP Clients contacts starred."
