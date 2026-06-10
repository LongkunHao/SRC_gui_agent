import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_005":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_005' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Quote" or obj.get("id") == "obj_040":
            text_align = obj.get("textAlign", "")
            if text_align == "left":
                return True, "Quote textAlign correctly set to 'left'."
            else:
                return False, f"Quote textAlign is '{text_align}', expected 'left'."

    return False, "No object with name 'Quote' (obj_040) found on slide_005."
