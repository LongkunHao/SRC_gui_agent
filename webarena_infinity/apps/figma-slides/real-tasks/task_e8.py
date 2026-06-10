import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    comments = state.get("comments", [])
    for comment in comments:
        if comment.get("userName") == "David Park" and "slide design" in comment.get("text", "").lower():
            return False, "David Park's comment about slide design still exists"

    return True, "David Park's comment about slide design has been deleted"
