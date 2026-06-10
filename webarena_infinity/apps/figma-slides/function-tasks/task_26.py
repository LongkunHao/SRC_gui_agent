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

    # Check that no object with name "Date" or id "obj_003" exists
    for obj in objects:
        if obj.get("name") == "Date" or obj.get("id") == "obj_003":
            return False, "Object 'Date' (obj_003) still exists on slide_001; it should have been deleted."

    # Check total object count is 2
    obj_count = len(objects)
    if obj_count != 2:
        return False, f"Slide_001 has {obj_count} objects, expected 2."

    return True, "Object 'Date' (obj_003) successfully deleted from slide_001; 2 objects remain."
