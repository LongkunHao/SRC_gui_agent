import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_006":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_006' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Section Title" or obj.get("id") == "obj_050":
            color = obj.get("color", "")
            if color == "#FFD700":
                return True, "Section Title color correctly set to '#FFD700'."
            else:
                return False, f"Section Title color is '{color}', expected '#FFD700'."

    return False, "No object with name 'Section Title' (obj_050) found on slide_006."
