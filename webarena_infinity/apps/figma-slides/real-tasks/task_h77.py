import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    directional_types = {"push", "slide_in", "slide_out", "move_in", "move_out"}
    directionless_types = {"dissolve", "smart_animate"}

    for s in state.get("slides", []):
        title = s.get("title", "")
        trans = s.get("transition", {})
        t_type = trans.get("type", "none")

        if t_type == "none":
            # Leave none transitions unchanged - only check easing
            if trans.get("easing") != "ease_in_out":
                errors.append(
                    f"'{title}' easing is '{trans.get('easing')}', expected 'ease_in_out'"
                )
            continue

        if trans.get("easing") != "ease_in_out":
            errors.append(
                f"'{title}' easing is '{trans.get('easing')}', expected 'ease_in_out'"
            )

        if t_type in directional_types:
            if trans.get("duration") != 500:
                errors.append(
                    f"'{title}' duration is {trans.get('duration')}, expected 500 "
                    f"(directional)"
                )
        elif t_type in directionless_types:
            if trans.get("duration") != 400:
                errors.append(
                    f"'{title}' duration is {trans.get('duration')}, expected 400 "
                    f"(directionless)"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Transition timing normalized: ease_in_out everywhere, duration by type"
