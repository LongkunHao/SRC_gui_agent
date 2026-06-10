import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find the title slide (Q4 2025 Product Strategy)
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Q4 2025 Product Strategy":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find title slide 'Q4 2025 Product Strategy'"

    objects = target_slide.get("objects", [])

    for obj in objects:
        name = obj.get("name", "")
        has_animation = obj.get("animation") is not None

        if has_animation:
            # Animated objects should have opacity 80
            opacity = obj.get("opacity")
            if opacity != 80:
                errors.append(f"'{name}' (animated) opacity is {opacity}, expected 80")
        else:
            # Non-animated objects should be locked
            if not obj.get("locked", False):
                errors.append(f"'{name}' (no animation) should be locked")

    if errors:
        return False, "; ".join(errors)
    return True, "Animated objects opacity 80; non-animated objects locked on title slide"
