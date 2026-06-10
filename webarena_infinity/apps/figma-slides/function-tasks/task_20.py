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
        if obj.get("name") == "Title" or obj.get("id") == "obj_001":
            locked = obj.get("locked")
            if locked is True:
                return True, "Title object correctly locked."
            else:
                return False, f"Title locked is {locked}, expected True."

    return False, "No object with name 'Title' (obj_001) found on slide_001."
