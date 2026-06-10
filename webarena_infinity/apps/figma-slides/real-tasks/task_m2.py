import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    comments = state.get("comments", [])

    if len(comments) == 0:
        return False, "No comments found in state"

    unresolved = []
    for comment in comments:
        if comment.get("resolved") is not True:
            author = comment.get("userName", "Unknown")
            text_preview = comment.get("text", "")[:50]
            unresolved.append(f"{author}: '{text_preview}'")

    if unresolved:
        return False, f"Found {len(unresolved)} unresolved comment(s): {'; '.join(unresolved)}"

    return True, f"All {len(comments)} comments are resolved"
