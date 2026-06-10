import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    comments = state.get("comments", [])

    # Check no comment from James O'Brien about competitive
    for comment in comments:
        if comment.get("userName") == "James O'Brien" and "competitive" in comment.get("text", "").lower():
            return False, "James O'Brien's comment about competitive comparison still exists"

    # Find Aiko's comment about token architecture and check resolved
    aiko_comment = None
    for comment in comments:
        if comment.get("userName") == "Aiko Tanaka" and "token" in comment.get("text", "").lower():
            aiko_comment = comment
            break

    if aiko_comment is None:
        return False, "Could not find Aiko Tanaka's comment about token architecture"

    if aiko_comment.get("resolved") is not True:
        return False, f"Aiko's token architecture comment is not resolved (resolved={aiko_comment.get('resolved')})"

    return True, "James's competitive comment deleted and Aiko's token comment resolved"
