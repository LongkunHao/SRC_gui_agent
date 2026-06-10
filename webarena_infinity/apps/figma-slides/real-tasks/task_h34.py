import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find Customer Feedback slide
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Customer Feedback":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Customer Feedback'"

    objects = target_slide.get("objects", [])

    for obj in objects:
        name = obj.get("name", "")
        anim = obj.get("animation")

        if name == "Attribution":
            # Should have slide_left animation, 500ms, after_previous
            if anim is None:
                errors.append("Attribution has no animation, expected slide_left")
                continue
            if anim.get("style") != "slide_left":
                errors.append(f"Attribution animation style is '{anim.get('style')}', expected 'slide_left'")
            if anim.get("duration") != 500:
                errors.append(f"Attribution animation duration is {anim.get('duration')}, expected 500")
            if anim.get("timing") != "after_previous":
                errors.append(f"Attribution animation timing is '{anim.get('timing')}', expected 'after_previous'")
        else:
            # All other objects should have no animation
            if anim is not None:
                errors.append(f"'{name}' should have no animation, but has {anim.get('style', 'unknown')}")

    if errors:
        return False, "; ".join(errors)
    return True, "Customer Feedback: all animations removed except Attribution (slide_left 500ms after_previous)"
