import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "API Reference":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'API Reference'"

    # Find the code object
    code_obj = None
    for obj in target.get("objects", []):
        if obj.get("type") == "code":
            code_obj = obj
            break

    if code_obj is None:
        return False, "Could not find a code object on API Reference slide"

    # Check language
    language = code_obj.get("language")
    if language != "Python":
        return False, f"Code language is '{language}', expected 'Python'"

    # Check theme
    theme = code_obj.get("theme", "")
    if theme.lower() != "github":
        return False, f"Code theme is '{theme}', expected 'github'"

    return True, "Code object language changed to Python and theme to GitHub"
