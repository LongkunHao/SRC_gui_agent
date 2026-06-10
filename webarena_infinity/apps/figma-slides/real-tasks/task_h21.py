import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Q4 Roadmap"
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Q4 Roadmap":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Q4 Roadmap'"

    # Check background is gradient with correct colors
    bg = target_slide.get("background", {})
    if bg.get("type") != "gradient":
        errors.append(f"Background type is '{bg.get('type')}', expected 'gradient'")
    else:
        gradient = bg.get("gradient", {})
        stops = gradient.get("stops", [])
        colors = [s.get("color", "").upper() for s in stops]
        if "#0A0A2A" not in colors:
            errors.append(f"Gradient missing color #0A0A2A, got stops: {stops}")
        if "#1E1E1E" not in colors:
            errors.append(f"Gradient missing color #1E1E1E, got stops: {stops}")

    # Check subtitle text
    subtitle = None
    for obj in target_slide.get("objects", []):
        if obj.get("name") == "Section Subtitle":
            subtitle = obj
            break

    if not subtitle:
        errors.append("Could not find 'Section Subtitle' object")
    else:
        text = subtitle.get("text", "")
        if text != "Innovation Starts Here":
            errors.append(f"Section Subtitle text is '{text}', expected 'Innovation Starts Here'")

    # Check transition
    trans = target_slide.get("transition", {})
    if trans.get("type") != "smart_animate":
        errors.append(f"Transition type is '{trans.get('type')}', expected 'smart_animate'")
    if trans.get("duration") != 600:
        errors.append(f"Transition duration is {trans.get('duration')}, expected 600")

    if errors:
        return False, "; ".join(errors)
    return True, "Q4 Roadmap: gradient background, subtitle updated, smart animate transition 600ms"
