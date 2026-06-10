import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    slide = next((s for s in slides if s.get("id") == "slide_008"), None)
    if not slide:
        return False, "Slide slide_008 not found."

    objects = slide.get("objects", [])
    obj = next((o for o in objects if o.get("id") == "obj_071"), None)
    if not obj:
        return False, "Object obj_071 (code block) not found on slide_008."

    theme = obj.get("theme")
    if theme != "dracula":
        return False, f"Expected code block obj_071 theme to be 'dracula', but found '{theme}'."

    return True, "Code block obj_071 on slide_008 has theme 'dracula' as expected."
