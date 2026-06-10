import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    default_transition = deck_settings.get("defaultTransition", {})

    t_type = default_transition.get("type", "")
    t_direction = default_transition.get("direction", "")

    if t_type != "push":
        return False, f"deckSettings.defaultTransition.type is '{t_type}', expected 'push'."
    if t_direction != "left":
        return False, f"deckSettings.defaultTransition.direction is '{t_direction}', expected 'left'."

    return True, "deckSettings.defaultTransition has type 'push' and direction 'left'."
