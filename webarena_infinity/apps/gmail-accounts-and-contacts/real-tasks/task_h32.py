# Task: Toggle star on each TechCorp contact.
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

    # Sarah Chen: was starred -> should now be unstarred
    sarah = contact_map.get("Sarah Chen")
    if sarah is None:
        errors.append("Sarah Chen not found")
    elif sarah.get("isStarred"):
        errors.append("Sarah Chen should be unstarred (was starred, should be toggled)")

    # Maya Patel: was starred -> should now be unstarred
    maya = contact_map.get("Maya Patel")
    if maya is None:
        errors.append("Maya Patel not found")
    elif maya.get("isStarred"):
        errors.append("Maya Patel should be unstarred (was starred, should be toggled)")

    # Patricia Wong-Anderson: was unstarred -> should now be starred
    patricia = contact_map.get("Patricia Wong-Anderson")
    if patricia is None:
        errors.append("Patricia Wong-Anderson not found")
    elif not patricia.get("isStarred"):
        errors.append(
            "Patricia Wong-Anderson should be starred (was unstarred, should be toggled)"
        )

    if errors:
        return False, "; ".join(errors)
    return True, "Star status toggled for all TechCorp contacts."
