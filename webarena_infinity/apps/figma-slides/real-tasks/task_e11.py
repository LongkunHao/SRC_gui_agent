import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    # Find the first slide (order 0 or title "Q4 2025 Product Strategy")
    target_slide = None
    for slide in slides:
        if slide.get("title") == "Q4 2025 Product Strategy" or slide.get("order") == 0:
            target_slide = slide
            break

    if target_slide is None:
        return False, "Could not find the first slide"

    objects = target_slide.get("objects", [])
    target_obj = None
    for obj in objects:
        if obj.get("name") == "Title":
            target_obj = obj
            break

    if target_obj is None:
        return False, "Could not find object named 'Title' on the first slide"

    if target_obj.get("locked") is not True:
        return False, f"Title object is not locked (locked={target_obj.get('locked')})"

    return True, "Main title on the first slide is locked"
