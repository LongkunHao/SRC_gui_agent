import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # The slide whose presenter notes warn about sensitive/external sharing
    # is Competitive Landscape (slide_013)
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Competitive Landscape":
            target_slide = s
            break

    if not target_slide:
        return False, "Competitive Landscape slide not found"

    # Should be skipped (hidden from presentation)
    if target_slide.get("skipped") is not True:
        errors.append("Competitive Landscape should be skipped")

    # All objects should be locked
    for obj in target_slide.get("objects", []):
        if obj.get("locked") is not True:
            errors.append(f"Object '{obj.get('name')}' is not locked")

    # Slide numbers should be disabled
    if target_slide.get("slideNumberEnabled") is not False:
        errors.append("Slide numbers should be disabled on Competitive Landscape")

    if errors:
        return False, "; ".join(errors)
    return True, "Sensitive slide skipped, all objects locked, slide numbers disabled"
