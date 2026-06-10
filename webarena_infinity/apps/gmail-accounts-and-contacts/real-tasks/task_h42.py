# Task: For non-US contacts, remove Work label if present and add Travel Contacts if missing.
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

    # Non-US contacts: Sophie Laurent (France), Yuki Tanaka (Japan),
    # Raj Kapoor (India), Elena Volkov (France)
    non_us = [
        ("Sophie Laurent", True, True),   # had Work -> remove, had Travel -> keep
        ("Yuki Tanaka", False, True),      # no Work, had Travel -> keep
        ("Raj Kapoor", True, False),       # had Work -> remove, no Travel -> add
        ("Elena Volkov", True, True),      # had Work -> remove, had Travel -> keep
    ]

    for name, had_work, had_travel in non_us:
        c = contact_map.get(name)
        if c is None:
            errors.append(f"Contact '{name}' not found")
            continue

        # Work label (clabel_3) should be removed from all non-US contacts that had it
        if had_work and "clabel_3" in c.get("labels", []):
            errors.append(f"'{name}' should not have Work label (non-US contact)")

        # Travel Contacts (clabel_11) should be present on all non-US contacts
        if "clabel_11" not in c.get("labels", []):
            errors.append(f"'{name}' should have Travel Contacts label")

    if errors:
        return False, "; ".join(errors)
    return True, "Non-US contacts updated: Work removed, Travel Contacts ensured."
