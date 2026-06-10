import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Agenda":
            bg = slide.get("background", {})
            bg_type = bg.get("type", "")
            bg_color = bg.get("color", "")

            if bg_type != "solid":
                return False, f"Slide 'Agenda' background type is '{bg_type}', expected 'solid'."
            if bg_color != "#2D2D2D":
                return False, f"Slide 'Agenda' background color is '{bg_color}', expected '#2D2D2D'."

            return True, "Slide 'Agenda' has background type 'solid' with color '#2D2D2D'."

    return False, "No slide with title 'Agenda' found."
