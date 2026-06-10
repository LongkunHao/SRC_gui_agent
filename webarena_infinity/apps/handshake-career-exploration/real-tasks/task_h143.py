"""
Task: Read your most recent unread top-match message. Then find the employer
whose alumni testimonial mentions 'ownership culture'. You don't currently
follow them — follow them and save their internship with the most applicants.

Discovery: Most recent unread top-match → msg_01 (Google, Mar 6).
'ownership culture' → Rachel Torres at Amazon: "Ownership culture is real here."
Amazon (emp_09) not followed. Most-applicant internship: job_08 (SDE Intern, 2103).

Verify:
(1) msg_01 isRead
(2) emp_09 in followedEmployerIds
(3) job_08 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})

    # Check 1: msg_01 read
    messages = state.get("messages", [])
    msg_01 = next((m for m in messages if m.get("id") == "msg_01"), None)
    if msg_01 is None:
        errors.append("msg_01 not found.")
    elif not msg_01.get("isRead"):
        errors.append("msg_01 not marked as read.")

    # Check 2: follow Amazon
    followed = user.get("followedEmployerIds", [])
    if "emp_09" not in followed:
        errors.append("emp_09 (Amazon) not in followedEmployerIds.")

    # Check 3: save job_08
    saved = user.get("savedJobIds", [])
    if "job_08" not in saved:
        errors.append(
            f"job_08 not in savedJobIds. Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "msg_01 read. Amazon followed (ownership culture testimonial). "
        "job_08 (SDE Intern, most applicants) saved."
    )
