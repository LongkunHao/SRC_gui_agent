"""
Task: Find the employer that lists 'GitHub' as an affiliated company.
Save both of their active internships and bookmark their feed post.

Discovery: GitHub affiliate → Microsoft (emp_03).
Active internships: job_04 (SWE Intern), job_23 (PM Intern).
Feed post: post_19 (Microsoft Imagine Cup).

Verify:
(1) job_04 in savedJobIds
(2) job_23 in savedJobIds
(3) post_19 bookmarked + in savedPostIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    posts = state.get("feedPosts", [])

    # Check 1-2: Microsoft internships saved
    saved = user.get("savedJobIds", [])
    for jid, title in [("job_04", "SWE Intern"), ("job_23", "PM Intern")]:
        if jid not in saved:
            errors.append(f"{jid} ({title}) not in savedJobIds.")

    # Check 3: post_19 bookmarked
    post_19 = next((p for p in posts if p.get("id") == "post_19"), None)
    if post_19 is None:
        errors.append("post_19 not found.")
    elif not post_19.get("bookmarked"):
        errors.append("post_19 not bookmarked.")

    if "post_19" not in user.get("savedPostIds", []):
        errors.append("post_19 not in savedPostIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Microsoft identified (GitHub affiliate). "
        "Both internships saved. Imagine Cup post bookmarked."
    )
