"""
Task: Read Stripe message, save Stripe internship, comment on Stripe's
engineering post, add Backend Developer to roles.

Discovery: msg_06 (Stripe, unread). job_09 (Stripe Backend Engineer Intern).
post_13 (Stripe engineering post). Add Backend Developer to roles.

Verify:
(1) msg_06.isRead == True
(2) job_09 in savedJobIds
(3) post_13 has new comment from Maya Chen
(4) "Backend Developer" in careerInterests.roles
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: msg_06.isRead == True
    messages = state.get("messages", [])
    msg_06 = None
    for msg in messages:
        if msg.get("id") == "msg_06":
            msg_06 = msg
            break
    if msg_06 is None:
        errors.append("msg_06 not found in messages")
    else:
        if not msg_06.get("isRead", False):
            errors.append("msg_06.isRead is not True")

    # Check 2: job_09 in savedJobIds
    saved_jobs = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_09" not in saved_jobs:
        errors.append("job_09 not found in savedJobIds")

    # Check 3: post_13 has new comment from Maya Chen
    feed_posts = state.get("feedPosts", [])
    post_13 = None
    for post in feed_posts:
        if post.get("id") == "post_13":
            post_13 = post
            break
    if post_13 is None:
        errors.append("post_13 not found in feedPosts")
    else:
        comments = post_13.get("comments", [])
        found_maya_comment = False
        for comment in comments:
            author = comment.get("authorName", "")
            if "Maya" in author:
                found_maya_comment = True
                break
        if not found_maya_comment:
            errors.append("No comment from Maya Chen found on post_13")

    # Check 4: "Backend Developer" in careerInterests.roles
    career_interests = state.get("currentUser", {}).get("careerInterests", {})
    roles = career_interests.get("roles", [])
    if "Backend Developer" not in roles:
        errors.append(f"'Backend Developer' not found in careerInterests.roles: {roles}")

    if errors:
        return False, " | ".join(errors)

    return True, "All checks passed: msg_06 read, job_09 saved, comment on post_13, Backend Developer added to roles."
