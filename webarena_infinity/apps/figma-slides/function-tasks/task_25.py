import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_015":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_015' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Title" or obj.get("id") == "obj_140":
            font_weight = obj.get("fontWeight")
            if font_weight == 600:
                return True, "Title fontWeight correctly set to 600."
            else:
                return False, f"Title fontWeight is {font_weight}, expected 600."

    return False, "No object with name 'Title' (obj_140) found on slide_015."
