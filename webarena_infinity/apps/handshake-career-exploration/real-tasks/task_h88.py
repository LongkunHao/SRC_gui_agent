"""
Task: Find employer with most followers. Like their post, bookmark it, save their active internships.

Discovery: Apple (emp_05) has 52,300 followers (most). Post: post_11 (seed likes=289,
bookmarked=false). Active internships: job_06, job_25.

Verify:
(1) post_11.likes > 289 (seed value)
(2) post_11.bookmarked == True
(3) post_11 id in savedPostIds
(4) job_06 in savedJobIds
(5) job_25 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check post_11 (Apple's post)
    feed_posts = state.get("feedPosts", [])
    post_11 = next((p for p in feed_posts if p.get("id") == "post_11"), None)

    if post_11 is None:
        errors.append("Post post_11 (Apple) not found in feedPosts.")
    else:
        # Check 1: likes > 289 (seed value)
        likes = post_11.get("likes", 0)
        if likes <= 289:
            errors.append(
                f"post_11 likes={likes}, expected > 289 (seed value). "
                f"Post was not liked."
            )

        # Check 2: bookmarked == True
        if post_11.get("bookmarked") is not True:
            errors.append(
                f"post_11 bookmarked={post_11.get('bookmarked')}, expected True."
            )

    # Check 3: post_11 in savedPostIds
    current_user = state.get("currentUser", {})
    saved_post_ids = current_user.get("savedPostIds", [])
    if "post_11" not in saved_post_ids:
        errors.append(
            f"post_11 not in savedPostIds. Current savedPostIds: {saved_post_ids}"
        )

    # Check 4-5: Apple active internships in savedJobIds
    saved_job_ids = current_user.get("savedJobIds", [])

    apple_internships = {
        "job_06": "Apple Hardware Engineering Intern",
        "job_25": "Apple Machine Learning Intern",
    }

    for job_id, job_title in apple_internships.items():
        if job_id not in saved_job_ids:
            errors.append(
                f"{job_title} ({job_id}) not in savedJobIds. "
                f"Current savedJobIds: {saved_job_ids}"
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Apple post (post_11) liked (likes={post_11.get('likes')}), bookmarked, "
        f"and in savedPostIds. Apple internships job_06 and job_25 saved."
    )
