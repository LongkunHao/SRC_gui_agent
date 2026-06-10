import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides = state.get("slides", [])

    # Find title slide "Q4 2025 Product Strategy"
    title_slide = None
    for s in slides:
        if s.get("title") == "Q4 2025 Product Strategy":
            title_slide = s
            break

    if not title_slide:
        return False, "Could not find slide titled 'Q4 2025 Product Strategy'"

    # Check ALL objects on title slide have animation == None/null
    title_objects = title_slide.get("objects", [])
    if not title_objects:
        errors.append("No objects found on title slide")
    else:
        for obj in title_objects:
            obj_name = obj.get("name", obj.get("id", "unknown"))
            anim = obj.get("animation")
            if anim is not None:
                errors.append(f"Title slide object '{obj_name}' has animation {anim}, expected None")

    # Find slide "Q4 Roadmap"
    roadmap_slide = None
    for s in slides:
        if s.get("title") == "Q4 Roadmap":
            roadmap_slide = s
            break

    if not roadmap_slide:
        errors.append("Could not find slide titled 'Q4 Roadmap'")
    else:
        # Find "Section Title" object
        objects = roadmap_slide.get("objects", [])
        section_title_obj = None
        for obj in objects:
            if obj.get("name") == "Section Title":
                section_title_obj = obj
                break

        if not section_title_obj:
            errors.append("Could not find 'Section Title' object on Q4 Roadmap slide")
        else:
            anim = section_title_obj.get("animation")
            if anim is None:
                errors.append("Section Title on Q4 Roadmap has no animation, expected scale")
            else:
                if anim.get("style") != "scale":
                    errors.append(f"Section Title animation style is '{anim.get('style')}', expected 'scale'")
                if anim.get("duration") != 500:
                    errors.append(f"Section Title animation duration is {anim.get('duration')}, expected 500")
                if anim.get("timing") != "on_click":
                    errors.append(f"Section Title animation timing is '{anim.get('timing')}', expected 'on_click'")

    if errors:
        return False, "; ".join(errors)
    return True, "Title slide animations removed, Q4 Roadmap section title has scale animation (500ms, on_click)"
