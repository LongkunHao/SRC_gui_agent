import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find post post_08 (Kevin O'Brien FAANG interview prep)
    posts = state.get("feedPosts", [])
    post_08 = None
    for post in posts:
        if post.get("id") == "post_08":
            post_08 = post
            break

    if post_08 is None:
        return False, "Post post_08 (Kevin O'Brien FAANG prep) not found in state."

    # post_08 is already in savedPostIds in seed data, so just check bookmarked == True on the post object
    bookmarked = post_08.get("bookmarked")
    if not bookmarked:
        return False, f"Post post_08 bookmarked is {bookmarked}, expected True."

    # Also verify it remains in savedPostIds
    current_user = state.get("currentUser", {})
    saved_post_ids = current_user.get("savedPostIds", [])
    if "post_08" not in saved_post_ids:
        return False, f"post_08 not found in savedPostIds: {saved_post_ids}"

    return True, "Post post_08 is bookmarked and in savedPostIds."
