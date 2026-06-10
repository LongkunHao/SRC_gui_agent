import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    slides = state.get("slides", [])
    total = len(slides)

    for slide in slides:
        if slide.get("title") == "Sprint Timeline":
            return False, f"Slide 'Sprint Timeline' still exists. Total slide count: {total}."

    if total != 15:
        return False, f"Total slide count is {total}, expected 15."

    return True, "Slide 'Sprint Timeline' has been deleted and total slide count is 15."
