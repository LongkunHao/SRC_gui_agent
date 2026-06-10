import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = next((s for s in slides if s.get("id") == "slide_001"), None)
    if not slide:
        return False, "Slide slide_001 not found."

    objects = slide.get("objects", [])
    obj = next((o for o in objects if o.get("id") == "obj_001"), None)
    if not obj:
        return False, "Object obj_001 (Title) not found on slide_001."

    animation = obj.get("animation")
    if animation is not None:
        return False, f"Expected obj_001 animation to be None (removed), but found {animation}."

    return True, "Object obj_001 (Title) on slide_001 has animation removed (None) as expected."
