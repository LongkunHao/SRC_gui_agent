import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find post post_19 (Microsoft Imagine Cup)
    posts = state.get("feedPosts", [])
    post_19 = None
    for post in posts:
        if post.get("id") == "post_19":
            post_19 = post
            break

    if post_19 is None:
        return False, "Post post_19 (Microsoft Imagine Cup) not found in state."

    likes = post_19.get("likes", 0)
    if likes <= 312:
        return False, f"Post post_19 likes is {likes}, expected > 312."

    return True, f"Successfully liked the Microsoft Imagine Cup post. likes={likes} > 312."
