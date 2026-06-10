import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Competitive Landscape":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Competitive Landscape'"

    # Find the Comparison Table object
    table_obj = None
    for obj in target.get("objects", []):
        if obj.get("name") == "Comparison Table":
            table_obj = obj
            break

    if table_obj is None:
        return False, "Could not find object named 'Comparison Table' on Competitive Landscape slide"

    # Check animation exists
    animation = table_obj.get("animation")
    if animation is None:
        return False, "Comparison Table has no animation (animation is None)"

    # Check animation style is slide_up
    anim_style = animation.get("style")
    if anim_style != "slide_up":
        return False, f"Animation style is '{anim_style}', expected 'slide_up'"

    # Check animation duration is 800
    anim_duration = animation.get("duration")
    if anim_duration != 800:
        return False, f"Animation duration is {anim_duration}, expected 800"

    return True, "Comparison Table has slide_up animation with 800ms duration"
