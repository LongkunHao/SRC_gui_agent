import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = next((s for s in slides if s.get("id") == "slide_007"), None)
    if not slide:
        return False, "Slide slide_007 not found."

    objects = slide.get("objects", [])
    obj = next((o for o in objects if o.get("id") == "obj_062"), None)
    if not obj:
        return False, "Object obj_062 (Timeline Badge) not found on slide_007."

    animation = obj.get("animation")
    if animation is None:
        return False, "Expected obj_062 to have an animation, but animation is None."

    duration = animation.get("duration")
    if duration != 600:
        return False, f"Expected obj_062 animation duration to be 600, but found {duration}."

    return True, "Object obj_062 (Timeline Badge) on slide_007 has animation duration 600 as expected."
