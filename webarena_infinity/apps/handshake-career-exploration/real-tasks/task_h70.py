"""
Task: Find the employer whose alumni testimonial mentions learning about
distributed systems. Save their active internship and bookmark their feed post.

Discovery: emp_10 (Stripe) testimonial by Marcus Johnson mentions
"distributed systems". Active internship: job_09 (Backend Engineer Intern).
Feed post: post_13.

Verify:
(1) job_09 in savedJobIds.
(2) post_13 bookmarked.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Stripe internship saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_09" not in saved:
        errors.append(
            f"job_09 (Stripe Backend Engineer Intern) not saved. "
            f"Current savedJobIds: {saved}"
        )

    # Check 2: Stripe feed post bookmarked
    posts = state.get("feedPosts", [])
    post_13 = next((p for p in posts if p.get("id") == "post_13"), None)
    if post_13 is None:
        errors.append("Post post_13 (Stripe) not found.")
    elif post_13.get("bookmarked") != True:
        errors.append(
            f"post_13 (Stripe) not bookmarked. bookmarked={post_13.get('bookmarked')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Stripe identified from 'distributed systems' testimonial. "
        "Internship (job_09) saved and feed post (post_13) bookmarked."
    )
