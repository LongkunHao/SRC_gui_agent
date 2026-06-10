import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # The slide whose notes say "highest priority" is Design System 2.0
    target = None
    for s in state.get("slides", []):
        if s.get("title") == "Design System 2.0":
            target = s
            break

    if not target:
        return False, "Design System 2.0 slide not found"

    # Template style should be Corporate Blue (ts_002)
    ts = target.get("templateStyle")
    if ts != "ts_002":
        errors.append(f"Template style is '{ts}', expected 'ts_002'")

    # Background should be solid white
    bg = target.get("background", {})
    if bg.get("type") != "solid":
        errors.append(f"Background type is '{bg.get('type')}', expected 'solid'")
    elif bg.get("color", "").upper() != "#FFFFFF":
        errors.append(f"Background color is '{bg.get('color')}', expected '#FFFFFF'")

    # Transition: push left, ease_in, 600ms
    trans = target.get("transition", {})
    if trans.get("type") != "push":
        errors.append(f"Transition type is '{trans.get('type')}', expected 'push'")
    if trans.get("direction") != "left":
        errors.append(f"Transition direction is '{trans.get('direction')}', expected 'left'")
    if trans.get("easing") != "ease_in":
        errors.append(f"Transition easing is '{trans.get('easing')}', expected 'ease_in'")
    if trans.get("duration") != 600:
        errors.append(f"Transition duration is {trans.get('duration')}, expected 600")

    if errors:
        return False, "; ".join(errors)
    return True, "Design System 2.0: Corporate Blue, white bg, push left ease_in 600ms"
