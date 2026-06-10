# Task: Remove Friends from Work contacts, add Friends to Family without it.
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

    # Marcus Williams had both Friends and Work -> Friends should be removed
    marcus = contact_map.get("Marcus Williams")
    if marcus is None:
        errors.append("Marcus Williams not found")
    elif "clabel_2" in marcus.get("labels", []):
        errors.append("Marcus Williams should not have Friends label (also has Work)")

    # Family contacts who should now have Friends (clabel_2):
    # Margaret Johnson, Richard Johnson, Laura Johnson-Martinez, Leo Martinez
    family_needs_friends = [
        "Margaret Johnson", "Richard Johnson",
        "Laura Johnson-Martinez", "Leo Martinez",
    ]
    for name in family_needs_friends:
        c = contact_map.get(name)
        if c is None:
            errors.append(f"{name} not found")
            continue
        if "clabel_2" not in c.get("labels", []):
            errors.append(f"{name} should have Friends label (has Family)")

    if errors:
        return False, "; ".join(errors)
    return True, "Friends removed from Work contacts, added to Family contacts."
