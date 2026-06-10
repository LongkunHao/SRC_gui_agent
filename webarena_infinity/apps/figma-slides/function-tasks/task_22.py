import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = None
    for s in slides:
        if s.get("id") == "slide_003":
            slide = s
            break
    if slide is None:
        return False, "Slide 'slide_003' not found."

    objects = slide.get("objects", [])
    for obj in objects:
        if obj.get("name") == "Metric Card 1" or obj.get("id") == "obj_021":
            fill = obj.get("fill", "")
            if fill == "#7B61FF":
                return True, "Metric Card 1 fill correctly set to '#7B61FF'."
            else:
                return False, f"Metric Card 1 fill is '{fill}', expected '#7B61FF'."

    return False, "No object with name 'Metric Card 1' (obj_021) found on slide_003."
