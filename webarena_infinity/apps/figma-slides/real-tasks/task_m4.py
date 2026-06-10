import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Next Steps":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Next Steps'"

    # Find the Action Items object
    action_items = None
    for obj in target.get("objects", []):
        if obj.get("name") == "Action Items":
            action_items = obj
            break

    if action_items is None:
        return False, "Could not find object named 'Action Items' on Next Steps slide"

    # Check animation exists with fade style
    animation = action_items.get("animation")
    if animation is None:
        return False, "Action Items object has no animation (animation is None)"

    anim_style = animation.get("style")
    if anim_style != "fade":
        return False, f"Animation style is '{anim_style}', expected 'fade'"

    # Check locked
    if action_items.get("locked") is not True:
        return False, f"Action Items object is not locked (locked={action_items.get('locked')})"

    return True, "Action Items has fade-in animation and is locked"
