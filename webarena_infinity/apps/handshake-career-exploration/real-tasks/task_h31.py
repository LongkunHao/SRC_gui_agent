"""
Task: Find the student who wrote about their first week at Stripe in the feed. Leave a comment
on their post asking about the onboarding process, then save any Stripe jobs you haven't saved yet.
Verify: (1) post_04 (Marcus Johnson) has a comment by Maya Chen containing 'onboarding'.
(2) job_09 (Stripe Backend Engineer Intern) is in currentUser.savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: post_04 has a comment by Maya Chen containing "onboarding"
    feed_posts = state.get("feedPosts", [])
    post_04 = next((p for p in feed_posts if p.get("id") == "post_04"), None)
    if post_04 is None:
        errors.append("Post post_04 (Marcus Johnson - Stripe first week) not found in feedPosts.")
    else:
        comments = post_04.get("comments", [])
        found_comment = False
        for comment in comments:
            author = comment.get("authorName", "")
            text = comment.get("text", "").lower()
            if "maya" in author.lower() and "onboarding" in text:
                found_comment = True
                break
        if not found_comment:
            errors.append(
                f"No comment from Maya Chen containing 'onboarding' found on post_04. "
                f"Current comments: {[{'authorName': c.get('authorName'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    # Check 2: job_09 in savedJobIds
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_09" not in saved_job_ids:
        errors.append(
            f"job_09 (Stripe Backend Engineer Intern) not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Comment with 'onboarding' by Maya Chen found on post_04 (Marcus Johnson). "
        "Stripe job job_09 is saved."
    )
