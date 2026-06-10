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
        if obj.get("name") == "Accent Line" or obj.get("id") == "obj_012":
            rotation = obj.get("rotation")
            if rotation == 45:
                return True, "Accent Line rotation correctly set to 45."
            else:
                return False, f"Accent Line rotation is {rotation}, expected 45."

    return False, "No object with name 'Accent Line' (obj_012) found on slide_002."
