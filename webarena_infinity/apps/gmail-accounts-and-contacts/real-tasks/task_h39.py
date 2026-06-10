# Task: Unlink Chrome and Google Play, turn off contacts/email sync, disable auto-save.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    linked_services = state.get("linkedServices", [])
    settings = state.get("accountSettings", {})
    sync = settings.get("syncSettings", {})

    # Chrome and Google Play should be unlinked
    for svc in linked_services:
        if svc.get("name") in ("Chrome", "Google Play"):
            if svc.get("isLinked"):
                errors.append(f"{svc.get('name')} should be unlinked")

    # Contacts sync and email sync should be off
    if sync.get("contactsSync") is not False:
        errors.append("Contacts sync should be disabled")
    if sync.get("emailSync") is not False:
        errors.append("Email sync should be disabled")

    # Auto-save contacts should be off
    if settings.get("autoSaveContacts") is not False:
        errors.append("Auto-save contacts should be disabled")

    if errors:
        return False, "; ".join(errors)
    return True, "Chrome and Play unlinked, sync disabled, auto-save off."
