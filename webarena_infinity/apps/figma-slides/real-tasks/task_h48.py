import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Team C Card (Mobile App, Status: Planning) on Resource Allocation
    for s in state.get("slides", []):
        if s.get("title") == "Resource Allocation":
            for obj in s.get("objects", []):
                if obj.get("name") == "Team C Card":
                    # Fill should be #3D1010
                    fill = obj.get("fill", "")
                    if fill.upper() != "#3D1010":
                        errors.append(f"Team C Card fill is '{fill}', expected '#3D1010'")

                    # Stroke color should be #FF6B6B
                    stroke = obj.get("stroke")
                    if not stroke:
                        errors.append("Team C Card has no stroke")
                    elif stroke.get("color", "").upper() != "#FF6B6B":
                        errors.append(
                            f"Team C Card stroke color is '{stroke.get('color')}', "
                            f"expected '#FF6B6B'"
                        )

                    # Animation: pop, 600ms, on_click
                    anim = obj.get("animation")
                    if not anim:
                        errors.append("Team C Card has no animation")
                    else:
                        if anim.get("style") != "pop":
                            errors.append(
                                f"Team C Card animation style is '{anim.get('style')}', "
                                f"expected 'pop'"
                            )
                        if anim.get("duration") != 600:
                            errors.append(
                                f"Team C Card animation duration is {anim.get('duration')}, "
                                f"expected 600"
                            )
                        if anim.get("timing") != "on_click":
                            errors.append(
                                f"Team C Card animation timing is '{anim.get('timing')}', "
                                f"expected 'on_click'"
                            )
                    break
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Team C Card (Planning): fill #3D1010, stroke #FF6B6B, pop animation 600ms"
