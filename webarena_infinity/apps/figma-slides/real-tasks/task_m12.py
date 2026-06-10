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

    # Check slideNumberEnabled
    sn_enabled = target.get("slideNumberEnabled")
    if sn_enabled is not True:
        return False, f"slideNumberEnabled is {sn_enabled}, expected True"

    # Check slideNumberFormat
    sn_format = target.get("slideNumberFormat")
    if sn_format != "with_total":
        return False, f"slideNumberFormat is '{sn_format}', expected 'with_total'"

    return True, "Thank You slide has slide numbers enabled with 'with_total' format"
