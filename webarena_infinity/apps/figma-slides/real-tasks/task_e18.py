import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    aspect_ratio = deck_settings.get("aspectRatio")

    if aspect_ratio != "4:3":
        return False, f"Aspect ratio is '{aspect_ratio}', expected '4:3'"

    return True, "Presentation aspect ratio set to 4:3"
