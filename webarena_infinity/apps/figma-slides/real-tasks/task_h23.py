import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Find Resource Allocation slide
    target_slide = None
    for s in state.get("slides", []):
        if s.get("title") == "Resource Allocation":
            target_slide = s
            break

    if not target_slide:
        return False, "Could not find slide titled 'Resource Allocation'"

    # Find Team B Card (Platform & API, the at-risk team)
    team_b = None
    for obj in target_slide.get("objects", []):
        if obj.get("name") == "Team B Card":
            team_b = obj
            break

    if not team_b:
        return False, "Could not find 'Team B Card' on Resource Allocation slide"

    # Check fill
    fill = team_b.get("fill", "")
    if fill.upper() != "#1A1A2E":
        errors.append(f"Team B Card fill is '{fill}', expected '#1A1A2E'")

    # Check animation
    anim = team_b.get("animation")
    if anim is None:
        errors.append("Team B Card has no animation, expected pop")
    else:
        if anim.get("style") != "pop":
            errors.append(f"Team B Card animation style is '{anim.get('style')}', expected 'pop'")
        if anim.get("duration") != 500:
            errors.append(f"Team B Card animation duration is {anim.get('duration')}, expected 500")
        if anim.get("timing") != "on_click":
            errors.append(f"Team B Card animation timing is '{anim.get('timing')}', expected 'on_click'")

    # Check Marcus Rivera's collaborator role changed to Viewer
    marcus = None
    for c in state.get("collaborators", []):
        if c.get("name") == "Marcus Rivera":
            marcus = c
            break

    if not marcus:
        errors.append("Collaborator 'Marcus Rivera' not found")
    else:
        if marcus.get("role") != "Viewer":
            errors.append(f"Marcus Rivera's role is '{marcus.get('role')}', expected 'Viewer'")

    if errors:
        return False, "; ".join(errors)
    return True, "Team B Card: fill #1A1A2E, pop animation 500ms on_click; Marcus Rivera role changed to Viewer"
