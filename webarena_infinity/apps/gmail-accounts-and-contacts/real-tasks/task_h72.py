# Task: Among TechCorp contacts, star Head of People Ops, unstar Engineering Manager.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Patricia Wong-Anderson (Head of People Operations) should be starred
    patricia = None
    for c in contacts:
        if c.get("firstName") == "Patricia" and c.get("lastName") == "Wong-Anderson":
            patricia = c
            break
    if patricia is None:
        errors.append("Patricia Wong-Anderson not found")
    elif not patricia.get("isStarred"):
        errors.append("Patricia Wong-Anderson (Head of People Ops) should be starred")

    # Maya Patel (Engineering Manager) should be unstarred
    maya = None
    for c in contacts:
        if c.get("firstName") == "Maya" and c.get("lastName") == "Patel":
            maya = c
            break
    if maya is None:
        errors.append("Maya Patel not found")
    elif maya.get("isStarred"):
        errors.append("Maya Patel (Engineering Manager) should be unstarred")

    # Sarah Chen (VP of Product) should still be starred
    sarah = None
    for c in contacts:
        if c.get("firstName") == "Sarah" and c.get("lastName") == "Chen":
            sarah = c
            break
    if sarah is None:
        errors.append("Sarah Chen not found")
    elif not sarah.get("isStarred"):
        errors.append("Sarah Chen (VP of Product) should still be starred")

    if errors:
        return False, "; ".join(errors)
    return True, "TechCorp contacts: Head of People Ops starred, Eng Manager unstarred."
