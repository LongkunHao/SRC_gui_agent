import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Next Steps":
            bg = slide.get("background", {})
            bg_type = bg.get("type", "")
            if bg_type != "gradient":
                return False, f"Slide 'Next Steps' background type is '{bg_type}', expected 'gradient'."

            gradient = bg.get("gradient", {})
            angle = gradient.get("angle")
            if angle != 90:
                return False, f"Slide 'Next Steps' gradient angle is {angle}, expected 90."

            stops = gradient.get("stops", [])
            stop_colors = [s.get("color", "") for s in stops]

            if "#1E1E1E" not in stop_colors:
                return False, f"Gradient stops missing '#1E1E1E'. Found colors: {stop_colors}."
            if "#0052CC" not in stop_colors:
                return False, f"Gradient stops missing '#0052CC'. Found colors: {stop_colors}."

            return True, "Slide 'Next Steps' has gradient background with angle 90 and stops #1E1E1E and #0052CC."

    return False, "No slide with title 'Next Steps' found."
