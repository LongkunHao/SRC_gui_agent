import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Q3 Highlights":
            transition = slide.get("transition", {})
            duration = transition.get("duration")

            if duration != 800:
                return False, f"Slide 'Q3 Highlights' transition duration is {duration}, expected 800."

            return True, "Slide 'Q3 Highlights' has transition duration of 800."

    return False, "No slide with title 'Q3 Highlights' found."
