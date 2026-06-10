import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Competitive Landscape":
            skipped = slide.get("skipped", False)
            if skipped is True:
                return True, "Slide 'Competitive Landscape' has skipped == True."
            return False, f"Slide 'Competitive Landscape' has skipped == {skipped}, expected True."

    return False, "No slide with title 'Competitive Landscape' found."
