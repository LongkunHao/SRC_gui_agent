import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Design System 2.0":
            transition = slide.get("transition", {})
            easing = transition.get("easing", "")

            if easing != "spring":
                return False, f"Slide 'Design System 2.0' transition easing is '{easing}', expected 'spring'."

            return True, "Slide 'Design System 2.0' has transition easing 'spring'."

    return False, "No slide with title 'Design System 2.0' found."
