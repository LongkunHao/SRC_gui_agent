import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    slides = state.get("slides", [])
    target = None
    for slide in slides:
        if slide.get("title") == "Sprint Timeline":
            target = slide
            break

    if target is None:
        return False, "Could not find slide with title 'Sprint Timeline'"

    if target.get("skipped") is not False:
        return False, f"Sprint Timeline slide is still skipped (skipped={target.get('skipped')})"

    return True, "Sprint Timeline slide has been unskipped"
