"""
Task: Find the employer whose alumni testimonial mentions 'patient care'.
Follow them, save their active job, and add 'Biotechnology' to your
preferred industries in career interests. Save your changes.

Discovery: 'patient care' → Epic Systems (emp_14), testimonial by Jenna Patel.
Active job: job_16 (Technical Solutions Engineer, Full-time).

Verify:
(1) emp_14 in followedEmployerIds
(2) job_16 in savedJobIds
(3) 'Biotechnology' in careerInterests.industries
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})

    followed = user.get("followedEmployerIds", [])
    if "emp_14" not in followed:
        errors.append(f"emp_14 (Epic Systems) not followed.")

    saved = user.get("savedJobIds", [])
    if "job_16" not in saved:
        errors.append(f"job_16 not in savedJobIds.")

    industries = user.get("careerInterests", {}).get("industries", [])
    if "Biotechnology" not in industries:
        errors.append(f"'Biotechnology' not in industries. Current: {industries}")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Epic Systems identified from 'patient care' testimonial. "
        "Followed, job_16 saved, Biotechnology added to industries."
    )
