import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find slide "Resource Allocation"
    slides = state.get("slides", [])
    target_slide = None
    for s in slides:
        if s.get("title") == "Resource Allocation":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Resource Allocation'"

    objects = target_slide.get("objects", [])
    card_names = ["Team A Card", "Team B Card", "Team C Card"]
    card_map = {}
    for obj in objects:
        name = obj.get("name", "")
        if name in card_names:
            card_map[name] = obj

    for card_name in card_names:
        if card_name not in card_map:
            errors.append(f"Object '{card_name}' not found on Resource Allocation slide")
            continue

        card = card_map[card_name]
        anim = card.get("animation")
        if anim is None:
            errors.append(f"{card_name} has no animation, expected bounce")
            continue

        if anim.get("style") != "bounce":
            errors.append(f"{card_name} animation style is '{anim.get('style')}', expected 'bounce'")
        if anim.get("duration") != 500:
            errors.append(f"{card_name} animation duration is {anim.get('duration')}, expected 500")
        if anim.get("timing") != "on_click":
            errors.append(f"{card_name} animation timing is '{anim.get('timing')}', expected 'on_click'")

    if errors:
        return False, "; ".join(errors)
    return True, "All three team cards on Resource Allocation have bounce animation (500ms, on_click)"
