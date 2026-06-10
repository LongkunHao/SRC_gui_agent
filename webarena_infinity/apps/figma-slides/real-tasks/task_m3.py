import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Customer Feedback":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Customer Feedback'"

    # Check background is solid #1A1A2E
    bg = target.get("background", {})
    bg_type = bg.get("type")
    if bg_type != "solid":
        return False, f"Background type is '{bg_type}', expected 'solid'"

    bg_color = bg.get("color", "")
    if bg_color.upper() != "#1A1A2E":
        return False, f"Background color is '{bg_color}', expected '#1A1A2E'"

    # Check transition is smart_animate
    transition = target.get("transition", {})
    t_type = transition.get("type")
    if t_type != "smart_animate":
        return False, f"Transition type is '{t_type}', expected 'smart_animate'"

    return True, "Customer Feedback slide has solid #1A1A2E background and smart_animate transition"
