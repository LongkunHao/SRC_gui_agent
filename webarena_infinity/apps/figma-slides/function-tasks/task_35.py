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

    code = obj.get("code")
    expected = 'console.log("Hello World");'
    if code != expected:
        return False, f"Expected code block obj_071 code to be '{expected}', but found '{code}'."

    return True, "Code block obj_071 on slide_008 has code 'console.log(\"Hello World\");' as expected."
