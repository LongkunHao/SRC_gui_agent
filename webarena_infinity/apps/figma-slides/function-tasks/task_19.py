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
        if obj.get("name") == "Date" or obj.get("id") == "obj_003":
            opacity = obj.get("opacity")
            if opacity == 50:
                return True, "Date opacity correctly set to 50."
            else:
                return False, f"Date opacity is {opacity}, expected 50."

    return False, "No object with name 'Date' (obj_003) found on slide_001."
