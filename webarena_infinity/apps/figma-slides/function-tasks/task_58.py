import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("id") == "slide_016":
            enabled = slide.get("slideNumberEnabled")
            if enabled is True:
                return True, "slide_016 ('Thank You') slideNumberEnabled is correctly True."
            else:
                return False, f"slide_016 slideNumberEnabled is {enabled}, expected True."

    return False, "Slide slide_016 ('Thank You') not found in state."
