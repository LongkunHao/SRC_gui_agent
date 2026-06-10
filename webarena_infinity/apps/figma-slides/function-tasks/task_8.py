import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    total = len(slides)

    if total != 17:
        return False, f"Total slide count is {total}, expected 17."

    new_slides = [s for s in slides if s.get("title") == "Untitled Slide"]
    if not new_slides:
        return False, "No slide with title 'Untitled Slide' found."

    new_slide = new_slides[0]
    layout = new_slide.get("layout", "")
    if layout != "layout_blank":
        return False, f"New slide has layout '{layout}', expected 'layout_blank'."

    order = new_slide.get("order")
    if order != 2:
        return False, f"New slide has order {order}, expected 2 (right after Agenda)."

    return True, "New 'Untitled Slide' exists with layout 'layout_blank' at order 2. Total count is 17."
