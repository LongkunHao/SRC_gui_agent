import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Customer Feedback":
            bg = slide.get("background", {})
            bg_type = bg.get("type", "")
            bg_color = bg.get("color", "")

            if bg_type != "solid":
                return False, f"Slide 'Customer Feedback' background type is '{bg_type}', expected 'solid'."
            if bg_color != "#2D1B69":
                return False, f"Slide 'Customer Feedback' background color is '{bg_color}', expected '#2D1B69'."

            return True, "Slide 'Customer Feedback' has background type 'solid' with color '#2D1B69'."

    return False, "No slide with title 'Customer Feedback' found."
