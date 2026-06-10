import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Meeting Agenda":
            return True, "Found slide with title 'Meeting Agenda'."

    titles = [s.get("title", "") for s in slides]
    return False, f"No slide with title 'Meeting Agenda' found. Current titles: {titles}"
