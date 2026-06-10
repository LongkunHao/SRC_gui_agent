import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check 1: A post by current user with audience='school' containing "case interview"
    feed_posts = state.get("feedPosts", [])
    current_user = state.get("currentUser", {})
    user_id = current_user.get("id", "")
    user_name = current_user.get("fullName", "")

    found_post = False
    for post in feed_posts:
        author_id = post.get("authorId", "")
        author_name = post.get("authorName", "")
        is_by_user = (author_id == user_id) or (author_name == user_name)
        if not is_by_user:
            continue
        audience = post.get("audience", "")
        content = post.get("content", "").lower()
        if audience == "school" and "case interview" in content:
            found_post = True
            break

    if not found_post:
        user_posts = [
            {"id": p.get("id"), "authorName": p.get("authorName"), "audience": p.get("audience"), "content": p.get("content", "")[:80]}
            for p in feed_posts
            if p.get("authorId") == user_id or p.get("authorName") == user_name
        ]
        errors.append(
            f"No post by {user_name} with audience='school' containing 'case interview' found. "
            f"User posts: {user_posts}"
        )

    # Check 2: evt_01 (McKinsey campus presentation) has rsvped == True
    events = state.get("events", [])
    evt_01 = next((e for e in events if e.get("id") == "evt_01"), None)
    if evt_01 is None:
        errors.append("Event evt_01 (McKinsey Campus Presentation) not found in events.")
    elif evt_01.get("rsvped") != True:
        errors.append(
            f"Event evt_01 (McKinsey Campus Presentation) is not RSVP'd. "
            f"rsvped={evt_01.get('rsvped')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Post by Maya Chen with audience='school' about case interviews found, "
        "and evt_01 (McKinsey Campus Presentation) is RSVP'd."
    )
