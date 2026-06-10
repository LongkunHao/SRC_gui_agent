import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Check Presentation Icons Pack is removed (0 styles, 0 variables)
    for lib in state.get("libraries", []):
        if lib.get("name") == "Presentation Icons Pack":
            errors.append("Presentation Icons Pack library still exists, should have been removed")
            break

    # Check code example theme is solarized
    api_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "API Reference":
            api_slide = s
            break

    if not api_slide:
        errors.append("Could not find slide titled 'API Reference'")
    else:
        code_obj = None
        for obj in api_slide.get("objects", []):
            if obj.get("type") == "code":
                code_obj = obj
                break
        if not code_obj:
            errors.append("No code object found on API Reference slide")
        else:
            theme = code_obj.get("theme")
            if theme != "solarized":
                errors.append(f"Code theme is '{theme}', expected 'solarized'")

    # Check Thank You slide transition
    ty_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Thank You":
            ty_slide = s
            break

    if not ty_slide:
        errors.append("Could not find slide titled 'Thank You'")
    else:
        trans = ty_slide.get("transition", {})
        if trans.get("type") != "push":
            errors.append(f"Thank You transition type is '{trans.get('type')}', expected 'push'")
        if trans.get("direction") != "bottom":
            errors.append(f"Thank You transition direction is '{trans.get('direction')}', expected 'bottom'")
        if trans.get("duration") != 500:
            errors.append(f"Thank You transition duration is {trans.get('duration')}, expected 500")

    if errors:
        return False, "; ".join(errors)
    return True, "No-styles library removed; code theme solarized; Thank You transition push-bottom 500ms"
