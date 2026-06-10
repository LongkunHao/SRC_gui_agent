import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    transition = deck_settings.get("defaultTransition", {})

    errors = []

    t_type = transition.get("type")
    if t_type != "push":
        errors.append(f"type is '{t_type}', expected 'push'")

    t_direction = transition.get("direction")
    if t_direction != "left":
        errors.append(f"direction is '{t_direction}', expected 'left'")

    t_duration = transition.get("duration")
    if t_duration != 600:
        errors.append(f"duration is {t_duration}, expected 600")

    if errors:
        return False, f"Default transition issues: {'; '.join(errors)}"

    return True, "Default deck transition set to push, left, 600ms"
