import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    share_settings = deck_settings.get("shareSettings", {})
    link_role = share_settings.get("linkRole")

    if link_role != "can_edit":
        return False, f"linkRole is '{link_role}', expected 'can_edit'"

    return True, "Link sharing permission changed to 'can_edit'"
