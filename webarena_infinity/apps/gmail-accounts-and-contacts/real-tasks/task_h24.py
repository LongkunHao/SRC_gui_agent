# Task: Look up Marcus Williams's company, move auto-saved contacts from that company.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    other_contacts = state.get("otherContacts", [])

    # Marcus Williams works at DesignHub
    # Tina Marshall (tina.marshall@designhub.com) is an auto-saved contact from DesignHub

    # Tina Marshall should now be in main contacts
    tina_in_main = any(
        c.get("email") == "tina.marshall@designhub.com" for c in contacts
    )
    if not tina_in_main:
        errors.append(
            "Tina Marshall (tina.marshall@designhub.com) not found in main contacts"
        )

    # Tina Marshall should no longer be in other contacts
    tina_in_other = any(
        c.get("email") == "tina.marshall@designhub.com" for c in other_contacts
    )
    if tina_in_other:
        errors.append(
            "Tina Marshall still in other contacts after being moved"
        )

    if errors:
        return False, "; ".join(errors)
    return True, "Tina Marshall moved from other contacts (DesignHub matches Marcus Williams's company)."
