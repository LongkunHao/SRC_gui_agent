import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Thank You":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Thank You'"

    transition = target.get("transition", {})
    transition_type = transition.get("type")

    if transition_type != "push":
        return False, f"Transition type is '{transition_type}', expected 'push'"

    return True, "Thank You slide transition type changed to push"
