import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Thank You":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Thank You'"

    slide_number_enabled = target.get("slideNumberEnabled")
    if slide_number_enabled is not False:
        return False, f"slideNumberEnabled is {slide_number_enabled}, expected False"

    return True, "Slide numbers disabled on Thank You slide"
