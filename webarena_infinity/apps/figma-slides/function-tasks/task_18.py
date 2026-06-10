import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_001":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_001' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Subtitle" or obj.get("id") == "obj_002":
            font_family = obj.get("fontFamily", "")
            if font_family == "DM Sans":
                return True, "Subtitle fontFamily correctly set to 'DM Sans'."
            else:
                return False, f"Subtitle fontFamily is '{font_family}', expected 'DM Sans'."

    return False, "No object with name 'Subtitle' (obj_002) found on slide_001."
