import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find Design System 2.0 slide
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Design System 2.0":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Design System 2.0'"

    objects = target_slide.get("objects", [])

    # Check Timeline Badge
    timeline = None
    ga = None
    for obj in objects:
        if obj.get("name") == "Timeline Badge":
            timeline = obj
        elif obj.get("name") == "GA Badge":
            ga = obj

    if not timeline:
        errors.append("Could not find 'Timeline Badge' object")
    else:
        text = timeline.get("text", "")
        if text != "Beta: Dec 2025":
            errors.append(f"Timeline Badge text is '{text}', expected 'Beta: Dec 2025'")
        fill = timeline.get("fill", "").upper()
        if fill != "#F24E1E":
            errors.append(f"Timeline Badge fill is '{fill}', expected '#F24E1E'")

    if not ga:
        errors.append("Could not find 'GA Badge' object")
    else:
        text = ga.get("text", "")
        if text != "GA: Mar 2026":
            errors.append(f"GA Badge text is '{text}', expected 'GA: Mar 2026'")
        fill = ga.get("fill", "").upper()
        if fill != "#FF6B35":
            errors.append(f"GA Badge fill is '{fill}', expected '#FF6B35'")

    if errors:
        return False, "; ".join(errors)
    return True, "Timeline Badge: 'Beta: Dec 2025' #F24E1E; GA Badge: 'GA: Mar 2026' #FF6B35"
