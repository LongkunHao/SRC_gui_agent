import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_014":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_014' not found."

    objects = slide.get("objects", [])

    # Check that no object with name "Risk 3" or id "obj_133" exists
    for obj in objects:
        if obj.get("name") == "Risk 3" or obj.get("id") == "obj_133":
            return False, "Object 'Risk 3' (obj_133) still exists on slide_014; it should have been deleted."

    # Check total object count is 3
    obj_count = len(objects)
    if obj_count != 3:
        return False, f"Slide_014 has {obj_count} objects, expected 3."

    return True, "Object 'Risk 3' (obj_133) successfully deleted from slide_014; 3 objects remain."
