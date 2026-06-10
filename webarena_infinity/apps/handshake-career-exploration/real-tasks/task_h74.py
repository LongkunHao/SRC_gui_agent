"""
Task: A student posted about choosing a startup over Big Tech. Like their post,
then save the startup job posting with the fewest applicants on Handshake.

Discovery: Jordan Taylor (post_12) wrote about choosing startup over Big Tech.
Startup-labeled jobs: job_09 (876 applicants), job_21 (89 applicants).
Fewest: job_21 (Startup Grind Labs, 89 applicants).

Verify:
(1) post_12.likes > 412 (seed value).
(2) job_21 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Jordan Taylor's post liked
    posts = state.get("feedPosts", [])
    post_12 = next((p for p in posts if p.get("id") == "post_12"), None)
    if post_12 is None:
        errors.append("Post post_12 (Jordan Taylor, startup) not found.")
    elif post_12.get("likes", 0) <= 412:
        errors.append(
            f"post_12 (Jordan Taylor) not liked. "
            f"likes={post_12.get('likes')}, expected > 412."
        )

    # Check 2: Startup job with fewest applicants saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_21" not in saved:
        errors.append(
            f"job_21 (Startup Grind Labs, 89 applicants - fewest startup job) "
            f"not saved. Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Jordan Taylor's startup post (post_12) liked. "
        "Startup job with fewest applicants (job_21, 89 applicants) saved."
    )
