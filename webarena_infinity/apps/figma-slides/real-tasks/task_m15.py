import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Thank You":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Thank You'"

    # Find the Closing Title object
    closing_title = None
    for obj in target.get("objects", []):
        if obj.get("name") == "Closing Title":
            closing_title = obj
            break

    if closing_title is None:
        return False, "Could not find object named 'Closing Title' on Thank You slide"

    # Check text
    text = closing_title.get("text", "")
    if text != "Questions?":
        return False, f"Closing Title text is '{text}', expected 'Questions?'"

    # Check fontSize
    font_size = closing_title.get("fontSize")
    if font_size != 48:
        return False, f"Closing Title fontSize is {font_size}, expected 48"

    return True, "Closing Title text changed to 'Questions?' with fontSize 48"
