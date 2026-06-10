import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    share_settings = deck_settings.get("shareSettings", {})

    errors = []

    link_access = share_settings.get("linkAccess")
    if link_access != "anyone":
        errors.append(f"linkAccess is '{link_access}', expected 'anyone'")

    link_role = share_settings.get("linkRole")
    if link_role != "can_edit":
        errors.append(f"linkRole is '{link_role}', expected 'can_edit'")

    if errors:
        return False, "; ".join(errors)

    return True, "Share settings updated: linkAccess='anyone', linkRole='can_edit'"
