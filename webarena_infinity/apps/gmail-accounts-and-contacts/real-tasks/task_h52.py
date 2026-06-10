# Task: Privacy + unlink + sync settings, add Emergency to tax-prep contact.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    settings = state.get("accountSettings", {})
    contacts = state.get("contacts", [])
    services = state.get("linkedServices", [])

    # Profile photo visibility should be contacts_only
    ps = settings.get("privacySettings", {})
    if ps.get("showProfilePhoto") != "contacts_only":
        errors.append(
            f"Profile photo visibility is '{ps.get('showProfilePhoto')}' "
            "instead of 'contacts_only'"
        )

    # Google Maps should be unlinked
    for svc in services:
        if svc.get("name") == "Google Maps" and svc.get("isLinked"):
            errors.append("Google Maps should be unlinked")

    # Email sync should be off
    ss = settings.get("syncSettings", {})
    if ss.get("emailSync") is not False:
        errors.append("Email sync should be disabled")

    # David Kim (notes mention tax prep) should have Emergency label
    david = None
    for c in contacts:
        if c.get("firstName") == "David" and c.get("lastName") == "Kim":
            david = c
            break
    if david is None:
        errors.append("David Kim not found")
    elif "clabel_10" not in david.get("labels", []):
        errors.append("David Kim should have Emergency label (handles tax prep)")

    if errors:
        return False, "; ".join(errors)
    return True, "Settings updated and Emergency label added to tax-prep contact."
