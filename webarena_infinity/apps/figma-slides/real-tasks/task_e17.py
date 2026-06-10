import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    # Look for the slide that was "Agenda" (order 1) — now should be "Meeting Agenda"
    target = None
    for slide in slides:
        if slide.get("title") == "Meeting Agenda":
            target = slide
            break

    if target is not None:
        return True, "Agenda slide renamed to 'Meeting Agenda'"

    # Check if "Agenda" still exists (meaning it was not renamed)
    for slide in slides:
        if slide.get("title") == "Agenda":
            return False, "Slide still has title 'Agenda', expected 'Meeting Agenda'"

    return False, "Could not find slide with title 'Meeting Agenda' or 'Agenda'"
