import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("id") == "slide_003":
            fmt = slide.get("slideNumberFormat")
            if fmt == "with_total":
                return True, "slide_003 ('Q3 Highlights') slideNumberFormat is correctly 'with_total'."
            else:
                return False, f"slide_003 slideNumberFormat is '{fmt}', expected 'with_total'."

    return False, "Slide slide_003 ('Q3 Highlights') not found in state."
