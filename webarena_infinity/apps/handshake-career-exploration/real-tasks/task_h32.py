"""
Task: Save all Microsoft jobs you haven't saved yet, then leave a comment on Microsoft's
Imagine Cup post in the feed expressing your interest in participating.
Verify: (1) job_04 and job_23 in savedJobIds.
(2) post_19 (Microsoft Imagine Cup) has a comment by Maya Chen.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Microsoft jobs saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    microsoft_jobs = {
        "job_04": "Software Engineer Intern (Microsoft)",
        "job_23": "Program Manager Intern (Microsoft)",
    }
    missing_jobs = []
    for job_id, job_title in microsoft_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Microsoft jobs not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 2: Comment by Maya Chen on post_19 (Imagine Cup)
    feed_posts = state.get("feedPosts", [])
    post_19 = next((p for p in feed_posts if p.get("id") == "post_19"), None)
    if post_19 is None:
        errors.append("Post post_19 (Microsoft Imagine Cup) not found in feedPosts.")
    else:
        comments = post_19.get("comments", [])
        found_comment = False
        for comment in comments:
            author = comment.get("authorName", "")
            if "maya" in author.lower():
                found_comment = True
                break
        if not found_comment:
            errors.append(
                f"No comment from Maya Chen found on post_19 (Microsoft Imagine Cup). "
                f"Current comments: {[{'authorName': c.get('authorName'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Microsoft jobs saved (job_04, job_23) and comment by Maya Chen "
        "found on post_19 (Microsoft Imagine Cup)."
    )
