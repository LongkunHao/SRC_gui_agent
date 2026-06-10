"""
Task: Find the nonprofit employer on Handshake. Follow them, save their active job,
and like their feed post.

Discovery: Teach For America (emp_18) is the only Nonprofit type employer.
Not followed in seed. Active job: job_20 (Corps Member FT).
Feed post: post_17 (98 likes).

Verify:
(1) emp_18 in followedEmployerIds.
(2) job_20 in savedJobIds.
(3) post_17.likes > 98.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: TFA followed
    followed = current_user.get("followedEmployerIds", [])
    if "emp_18" not in followed:
        errors.append(
            f"emp_18 (Teach For America) not in followedEmployerIds. "
            f"Current: {followed}"
        )

    # Check 2: TFA job saved
    saved_job_ids = current_user.get("savedJobIds", [])
    if "job_20" not in saved_job_ids:
        errors.append(
            f"job_20 (TFA Corps Member) not in savedJobIds. Current: {saved_job_ids}"
        )

    # Check 3: TFA post liked
    feed_posts = state.get("feedPosts", [])
    post_17 = next((p for p in feed_posts if p.get("id") == "post_17"), None)
    if post_17 is None:
        errors.append("Post post_17 (Teach For America) not found.")
    else:
        likes = post_17.get("likes", 0)
        if likes <= 98:
            errors.append(
                f"post_17 (TFA) likes={likes}, expected > 98 (seed=98)."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Teach For America (nonprofit) followed (emp_18), "
        "job saved (job_20), and post liked (post_17)."
    )
