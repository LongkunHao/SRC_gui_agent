import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Q4 2025 Product Strategy":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Q4 2025 Product Strategy'"

    bg = target.get("background", {})
    bg_type = bg.get("type")
    bg_color = bg.get("color", "")

    if bg_type != "solid":
        return False, f"Background type is '{bg_type}', expected 'solid'"

    if bg_color.upper() != "#2D1B69":
        return False, f"Background color is '{bg_color}', expected '#2D1B69'"

    return True, "Title slide background color changed to #2D1B69"
