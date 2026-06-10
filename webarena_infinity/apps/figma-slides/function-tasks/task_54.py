import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    deck_settings = state.get("deckSettings", {})
    aspect_ratio = deck_settings.get("aspectRatio")
    width = deck_settings.get("width")
    height = deck_settings.get("height")

    errors = []
    if aspect_ratio != "4:3":
        errors.append(f"aspectRatio is '{aspect_ratio}', expected '4:3'")
    if width != 1024:
        errors.append(f"width is {width}, expected 1024")
    if height != 768:
        errors.append(f"height is {height}, expected 768")

    if errors:
        return False, "; ".join(errors) + "."

    return True, "Deck settings correctly updated to 4:3 aspect ratio (1024x768)."
