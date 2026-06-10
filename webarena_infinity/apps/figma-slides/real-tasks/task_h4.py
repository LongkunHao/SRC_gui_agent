import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find title slide "Q4 2025 Product Strategy"
    slides = state.get("slides", [])
    title_slide = None
    for s in slides:
        if s.get("title") == "Q4 2025 Product Strategy":
            title_slide = s
            break

    if not title_slide:
        return False, "Could not find slide titled 'Q4 2025 Product Strategy'"

    # Check all objects are locked
    objects = title_slide.get("objects", [])
    if not objects:
        errors.append("No objects found on title slide")
    else:
        for obj in objects:
            obj_name = obj.get("name", obj.get("id", "unknown"))
            if not obj.get("locked", False):
                errors.append(f"Object '{obj_name}' is not locked")

    # Check slideNumberEnabled == False
    if title_slide.get("slideNumberEnabled") is not False:
        errors.append(f"slideNumberEnabled is {title_slide.get('slideNumberEnabled')}, expected False")

    # Check transition
    transition = title_slide.get("transition", {})
    t_type = transition.get("type", "")
    t_duration = transition.get("duration")
    if t_type != "dissolve":
        errors.append(f"Transition type is '{t_type}', expected 'dissolve'")
    if t_duration != 800:
        errors.append(f"Transition duration is {t_duration}, expected 800")

    if errors:
        return False, "; ".join(errors)
    return True, "Title slide: all objects locked, slide number disabled, dissolve transition at 800ms"
