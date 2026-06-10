import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target_slide = None
    for slide in slides:
        if slide.get("title") == "Q4 Roadmap":
            target_slide = slide
            break

    if target_slide is None:
        return False, "Could not find slide with title 'Q4 Roadmap'"

    objects = target_slide.get("objects", [])
    target_obj = None
    for obj in objects:
        if obj.get("name") == "Section Title":
            target_obj = obj
            break

    if target_obj is None:
        return False, "Could not find object named 'Section Title' on Q4 Roadmap slide"

    font_size = target_obj.get("fontSize")
    if font_size != 72:
        return False, f"Section Title fontSize is {font_size}, expected 72"

    return True, "Section Title font size on Q4 Roadmap slide changed to 72"
