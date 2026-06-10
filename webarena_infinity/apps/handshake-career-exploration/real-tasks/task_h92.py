"""
Task: Find employer with GitHub affiliate. Save their active jobs, comment on Imagine Cup
post, add Cloud Engineer to roles.

Discovery: Microsoft (emp_03) affiliates include GitHub. Active jobs: job_04, job_23.
Imagine Cup post: post_19.

Verify:
(1) job_04 in savedJobIds
(2) job_23 in savedJobIds
(3) post_19 has new comment from Maya Chen
(4) "Cloud Engineer" in careerInterests.roles
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    current_user = state.get("currentUser", {})
    saved_job_ids = current_user.get("savedJobIds", [])

    # Check 1: job_04 in savedJobIds
    if "job_04" not in saved_job_ids:
        errors.append(
            f"job_04 (Microsoft Software Engineer Intern) not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 2: job_23 in savedJobIds
    if "job_23" not in saved_job_ids:
        errors.append(
            f"job_23 (Microsoft Program Manager Intern) not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 3: post_19 has new comment from Maya Chen
    feed_posts = state.get("feedPosts", [])
    post_19 = next((p for p in feed_posts if p.get("id") == "post_19"), None)
    if post_19 is None:
        errors.append("Post post_19 (Microsoft Imagine Cup) not found in feedPosts.")
    else:
        comments = post_19.get("comments", [])
        # Seed has 1 comment (cmt_17 from Omar Hassan). Look for new comment from Maya Chen.
        maya_comments = [
            c for c in comments
            if "maya" in (c.get("authorName") or "").lower()
        ]
        if not maya_comments:
            errors.append(
                f"No comment from Maya Chen found on post_19 (Imagine Cup). "
                f"Current comments: {[{'authorName': c.get('authorName'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    # Check 4: "Cloud Engineer" in careerInterests.roles
    career = current_user.get("careerInterests", {})
    roles = career.get("roles", [])
    if "Cloud Engineer" not in roles:
        errors.append(
            f"'Cloud Engineer' not in careerInterests.roles. Current roles: {roles}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Microsoft (GitHub affiliate) active jobs saved (job_04, job_23), "
        "comment left on Imagine Cup post (post_19), "
        "and 'Cloud Engineer' added to career roles."
    )
