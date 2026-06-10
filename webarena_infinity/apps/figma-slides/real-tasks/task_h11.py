import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "API Reference"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "API Reference":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'API Reference'"

    # Find code object
    objects = target_slide.get("objects", [])
    code_obj = None
    for obj in objects:
        if obj.get("type") == "code":
            code_obj = obj
            break

    if not code_obj:
        return False, "Could not find code object on API Reference slide"

    # Check language
    language = code_obj.get("language", "")
    if language != "TypeScript":
        errors.append(f"Code language is '{language}', expected 'TypeScript'")

    # Check theme
    theme = code_obj.get("theme", "")
    if theme != "github":
        errors.append(f"Code theme is '{theme}', expected 'github'")

    # Check fontSize
    font_size = code_obj.get("fontSize")
    if font_size != 16:
        errors.append(f"Code fontSize is {font_size}, expected 16")

    if errors:
        return False, "; ".join(errors)
    return True, "Code object updated: TypeScript language, github theme, fontSize 16"
