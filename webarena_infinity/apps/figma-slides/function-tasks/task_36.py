import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = next((s for s in slides if s.get("id") == "slide_002"), None)
    if not slide:
        return False, "Slide slide_002 not found."

    objects = slide.get("objects", [])
    obj = next((o for o in objects if o.get("id") == "obj_011"), None)
    if not obj:
        return False, "Object obj_011 (Agenda List) not found on slide_002."

    animation = obj.get("animation")
    if animation is None:
        return False, "Expected obj_011 to have an animation, but animation is None."

    style = animation.get("style")
    if style != "bounce":
        return False, f"Expected obj_011 animation style to be 'bounce', but found '{style}'."

    return True, "Object obj_011 (Agenda List) on slide_002 has animation style 'bounce' as expected."
