"""
Task: Pivot your career interests toward AI safety research: change your
career community to 'Science & Research', add 'Research Scientist' to your
roles, and add 'Research' to your job functions. Then save both active jobs
from the AI safety company you already follow.

Discovery: AI safety company you follow → Anthropic (emp_15).
Active jobs: job_12 (Research Engineer Intern, already saved),
             job_29 (Policy Research Intern, not saved).

Verify:
(1) careerCommunity = 'Science & Research'
(2) 'Research Scientist' in roles
(3) 'Research' in jobFunctions
(4) job_12 in savedJobIds
(5) job_29 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    ci = user.get("careerInterests", {})

    # Check 1: career community
    if ci.get("careerCommunity") != "Science & Research":
        errors.append(
            f"careerCommunity is '{ci.get('careerCommunity')}', "
            "expected 'Science & Research'."
        )

    # Check 2: Research Scientist in roles
    roles = ci.get("roles", [])
    if "Research Scientist" not in roles:
        errors.append(
            f"'Research Scientist' not in roles. Current: {roles}"
        )

    # Check 3: Research in jobFunctions
    jf = ci.get("jobFunctions", [])
    if "Research" not in jf:
        errors.append(f"'Research' not in jobFunctions. Current: {jf}")

    # Check 4-5: both Anthropic jobs saved
    saved = user.get("savedJobIds", [])
    for jid in ["job_12", "job_29"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Career pivoted to Science & Research. Research Scientist role "
        "and Research function added. Both Anthropic jobs saved."
    )
