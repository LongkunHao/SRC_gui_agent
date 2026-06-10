import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check Sprint Timeline slide is deleted
    slides = state.get("slides", [])
    for slide in slides:
        if slide.get("title") == "Sprint Timeline":
            return False, "Slide 'Sprint Timeline' still exists but should be deleted"

    # Find Elena's comment about mobile team and check it's resolved
    comments = state.get("comments", [])
    elena_comment = None
    for comment in comments:
        if comment.get("userName") == "Elena Kowalski" and "mobile team" in comment.get("text", "").lower():
            elena_comment = comment
            break

    if elena_comment is None:
        return False, "Could not find Elena Kowalski's comment about mobile team"

    if elena_comment.get("resolved") is not True:
        return False, f"Elena's mobile team comment is not resolved (resolved={elena_comment.get('resolved')})"

    return True, "Sprint Timeline slide deleted and Elena's mobile team comment resolved"
