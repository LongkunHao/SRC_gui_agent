import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    comments = state.get("comments", [])
    target = None
    for comment in comments:
        if comment.get("userName") == "Marcus Rivera" and "uptime" in comment.get("text", "").lower():
            target = comment
            break

    if target is None:
        return False, "Could not find Marcus Rivera's comment about uptime"

    if target.get("resolved") is not True:
        return False, f"Marcus's uptime comment is not resolved (resolved={target.get('resolved')})"

    return True, "Marcus Rivera's comment about uptime is resolved"
