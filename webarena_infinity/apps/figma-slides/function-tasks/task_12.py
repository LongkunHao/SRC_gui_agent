import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Agenda":
            transition = slide.get("transition", {})
            t_type = transition.get("type", "")
            t_direction = transition.get("direction", "")

            if t_type != "push":
                return False, f"Slide 'Agenda' transition type is '{t_type}', expected 'push'."
            if t_direction != "left":
                return False, f"Slide 'Agenda' transition direction is '{t_direction}', expected 'left'."

            return True, "Slide 'Agenda' has transition type 'push' with direction 'left'."

    return False, "No slide with title 'Agenda' found."
