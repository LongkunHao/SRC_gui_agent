# Task: Add VIP Clients label to every starred Work contact who doesn't already have it.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Starred + Work (clabel_3) contacts that should gain VIP Clients (clabel_4):
    # Marcus Williams, Priya Sharma, Kevin Zhao, Maya Patel
    should_have_vip = [
        "Marcus Williams",
        "Priya Sharma",
        "Kevin Zhao",
        "Maya Patel",
    ]

    # Contacts that already had VIP Clients and should still have it:
    already_had_vip = ["Sarah Chen", "Emily Rodriguez"]

    contact_map = {}
    for c in contacts:
        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        contact_map[name] = c

    for name in should_have_vip + already_had_vip:
        contact = contact_map.get(name)
        if contact is None:
            errors.append(f"Contact '{name}' not found")
            continue
        if "clabel_4" not in contact.get("labels", []):
            errors.append(
                f"'{name}' (starred + Work) should have VIP Clients label but does not"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "VIP Clients label added to all starred Work contacts."
