import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Most-slides presentation: all transitions changed to dissolve/500ms."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    slides = state.get("slides", [])

    # pres_013 (Mobile Design System Components) has the most slides (25)
    target_pid = "pres_013"
    target_slides = [s for s in slides if s.get("presentationId") == target_pid]

    if not target_slides:
        return False, f"No slides found for {target_pid}"

    errors = []
    for s in target_slides:
        t = s.get("transition", {})
        sid = s.get("id")
        if t.get("type") != "dissolve":
            errors.append(
                f"{sid}: transition type should be 'dissolve', got '{t.get('type')}'"
            )
        if t.get("duration") != 500:
            errors.append(
                f"{sid}: transition duration should be 500, got {t.get('duration')}"
            )

    if errors:
        return False, f"{len(errors)} slides have wrong transitions: " + "; ".join(errors[:5])

    return True, (
        f"All {len(target_slides)} slides of pres_013 (most slides) "
        f"have transition dissolve/500ms."
    )
