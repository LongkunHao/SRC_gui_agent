import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Q4 Roadmap":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Q4 Roadmap'"

    # Check background is solid #0052CC
    bg = target.get("background", {})
    bg_type = bg.get("type")
    if bg_type != "solid":
        return False, f"Background type is '{bg_type}', expected 'solid'"

    bg_color = bg.get("color", "")
    if bg_color.upper() != "#0052CC":
        return False, f"Background color is '{bg_color}', expected '#0052CC'"

    # Find Section Subtitle object and check text
    subtitle_obj = None
    for obj in target.get("objects", []):
        if obj.get("name") == "Section Subtitle":
            subtitle_obj = obj
            break

    if subtitle_obj is None:
        return False, "Could not find object named 'Section Subtitle' on Q4 Roadmap slide"

    text = subtitle_obj.get("text", "")
    if text != "Building the next generation":
        return False, f"Section Subtitle text is '{text}', expected 'Building the next generation'"

    return True, "Q4 Roadmap background is #0052CC and subtitle updated"
