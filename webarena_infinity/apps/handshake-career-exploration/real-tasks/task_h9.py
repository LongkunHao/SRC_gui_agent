"""
Task: Bookmark all employer posts in the feed that are from companies you're currently following.
Verify: All feedPosts with authorType=='employer' and authorId in the seed followedEmployerIds
have bookmarked==True.

Seed followedEmployerIds: emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15.
Employer posts from followed companies:
- post_01 (Google, emp_01)
- post_03 (Meta, emp_07)
- post_05 (Anthropic, emp_15)
- post_11 (Apple, emp_05)
- post_13 (Stripe, emp_10)
- post_19 (Microsoft, emp_03)
"""

import requests


SEED_FOLLOWED_EMPLOYER_IDS = [
    "emp_01", "emp_03", "emp_05", "emp_07", "emp_10", "emp_12", "emp_15"
]


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])

    # Find all employer posts from followed companies
    target_posts = []
    for post in feed_posts:
        if (
            post.get("authorType") == "employer"
            and post.get("authorId") in SEED_FOLLOWED_EMPLOYER_IDS
        ):
            target_posts.append(post)

    if not target_posts:
        return False, (
            "No employer posts from followed companies found in feedPosts. "
            "This is unexpected; the seed data should contain such posts."
        )

    not_bookmarked = []
    for post in target_posts:
        if post.get("bookmarked") != True:
            not_bookmarked.append(
                f"{post.get('authorName', 'Unknown')} ({post.get('id')})"
            )

    if not_bookmarked:
        return False, (
            f"Not all employer posts from followed companies are bookmarked. "
            f"Not bookmarked: {', '.join(not_bookmarked)}. "
            f"Total target posts: {len(target_posts)}"
        )

    bookmarked_ids = [p.get("id") for p in target_posts]
    return True, (
        f"All {len(target_posts)} employer posts from followed companies are "
        f"bookmarked: {bookmarked_ids}"
    )
