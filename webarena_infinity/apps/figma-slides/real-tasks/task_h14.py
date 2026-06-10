import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Key Risks & Mitigations"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "Key Risks & Mitigations":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Key Risks & Mitigations'"

    objects = target_slide.get("objects", [])
    risk_names = ["Risk 1", "Risk 2", "Risk 3"]
    risk_map = {}
    for obj in objects:
        name = obj.get("name", "")
        if name in risk_names:
            risk_map[name] = obj

    for risk_name in risk_names:
        if risk_name not in risk_map:
            errors.append(f"Object '{risk_name}' not found on Key Risks & Mitigations slide")
            continue

        obj = risk_map[risk_name]

        # Check locked
        if not obj.get("locked", False):
            errors.append(f"{risk_name} is not locked")

        # Check cornerRadius
        cr = obj.get("cornerRadius")
        if cr != 16:
            errors.append(f"{risk_name} cornerRadius is {cr}, expected 16")

        # Check animation
        anim = obj.get("animation")
        if anim is None:
            errors.append(f"{risk_name} has no animation, expected fade")
            continue

        if anim.get("style") != "fade":
            errors.append(f"{risk_name} animation style is '{anim.get('style')}', expected 'fade'")
        if anim.get("duration") != 400:
            errors.append(f"{risk_name} animation duration is {anim.get('duration')}, expected 400")
        if anim.get("timing") != "on_click":
            errors.append(f"{risk_name} animation timing is '{anim.get('timing')}', expected 'on_click'")

    if errors:
        return False, "; ".join(errors)
    return True, "All three risk cards: locked, cornerRadius 16, fade animation 400ms on_click"
