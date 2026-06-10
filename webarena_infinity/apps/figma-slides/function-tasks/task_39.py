import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    comments = state.get("comments", [])
    if len(comments) != 7:
        return False, f"Expected 7 comments (6 seed + 1 new), but found {len(comments)}."

    matching = [
        c for c in comments
        if c.get("slideId") == "slide_006"
        and c.get("text") == "We should add budget numbers here."
    ]

    if not matching:
        return False, "No comment found with slideId 'slide_006' and text 'We should add budget numbers here.'."

    return True, "Found new comment on slide_006 with text 'We should add budget numbers here.' and total comments is 7."
