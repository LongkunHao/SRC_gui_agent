# Task: Two EuroDesign contacts — delete the UX Research Lead, star the other.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])

    # Elena Volkov is UX Research Lead at EuroDesign -> should be deleted
    for c in contacts:
        if c.get("firstName") == "Elena" and c.get("lastName") == "Volkov":
            errors.append("Elena Volkov (UX Research Lead) should have been deleted")

    # Sophie Laurent is Conference Director at EuroDesign -> should be starred
    sophie = None
    for c in contacts:
        if c.get("firstName") == "Sophie" and c.get("lastName") == "Laurent":
            sophie = c
            break

    if sophie is None:
        errors.append("Sophie Laurent not found (should not have been deleted)")
    elif not sophie.get("isStarred"):
        errors.append("Sophie Laurent should be starred")

    if errors:
        return False, "; ".join(errors)
    return True, "Elena Volkov deleted, Sophie Laurent starred."
