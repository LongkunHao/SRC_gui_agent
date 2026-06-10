import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target_slide = None
    for slide in slides:
        if slide.get("title") == "API Reference":
            target_slide = slide
            break

    if target_slide is None:
        return False, "Could not find slide with title 'API Reference'"

    objects = target_slide.get("objects", [])
    code_obj = None
    for obj in objects:
        if obj.get("type") == "code":
            code_obj = obj
            break

    if code_obj is None:
        return False, "Could not find a code object on the API Reference slide"

    theme = code_obj.get("theme", "")
    if theme.lower() != "dracula":
        return False, f"Code theme is '{theme}', expected 'dracula'"

    return True, "Code example theme changed to Dracula"
