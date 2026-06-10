import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_002":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_002' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Title" or obj.get("id") == "obj_010":
            font_size = obj.get("fontSize")
            if font_size == 42:
                return True, "Title fontSize correctly set to 42."
            else:
                return False, f"Title fontSize is {font_size}, expected 42."

    return False, "No object with name 'Title' (obj_010) found on slide_002."
