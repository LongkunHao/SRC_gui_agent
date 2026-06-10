import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Sprint Timeline":
            skipped = slide.get("skipped", False)
            if skipped is False or skipped is None:
                return True, "Slide 'Sprint Timeline' has skipped == False (unskipped)."
            return False, f"Slide 'Sprint Timeline' has skipped == {skipped}, expected False."

    return False, "No slide with title 'Sprint Timeline' found."
