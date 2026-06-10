import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find post post_05 (Anthropic AI safety internship applications)
    posts = state.get("feedPosts", [])
    post_05 = None
    for post in posts:
        if post.get("id") == "post_05":
            post_05 = post
            break

    if post_05 is None:
        return False, "Post post_05 (Anthropic AI safety) not found in state."

    likes = post_05.get("likes", 0)
    if likes <= 198:
        return False, f"Post post_05 likes is {likes}, expected > 198."

    return True, f"Successfully liked the Anthropic AI safety post. likes={likes} > 198."
