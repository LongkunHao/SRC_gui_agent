"""
Task: Add 'Fellowship' and 'Gap year' to your post-graduation plans in career interests,
add 'Exploring' to how Handshake can help you, and change your expected graduation to
'December 2026'. Save your changes.

Seed: postGraduation=['Working', 'Grad school'], helpWith=['Internship', 'Events', 'Network'],
      expectedGraduationDate='May 2027'.

Verify:
(1) 'Fellowship' in postGraduation.
(2) 'Gap year' in postGraduation.
(3) 'Exploring' in helpWith.
(4) expectedGraduationDate == 'December 2026'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    ci = state.get("currentUser", {}).get("careerInterests", {})
    errors = []

    # Check 1 & 2: Post-graduation plans
    post_grad = ci.get("postGraduation", [])
    if "Fellowship" not in post_grad:
        errors.append(f"'Fellowship' not in postGraduation. Current: {post_grad}")
    if "Gap year" not in post_grad:
        errors.append(f"'Gap year' not in postGraduation. Current: {post_grad}")

    # Check 3: helpWith
    help_with = ci.get("helpWith", [])
    if "Exploring" not in help_with:
        errors.append(f"'Exploring' not in helpWith. Current: {help_with}")

    # Check 4: Expected graduation date
    grad_date = ci.get("expectedGraduationDate", "")
    if grad_date != "December 2026":
        errors.append(
            f"expectedGraduationDate='{grad_date}', expected 'December 2026'."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Career interests updated: Fellowship and Gap year added to postGraduation, "
        "Exploring added to helpWith, expectedGraduationDate set to December 2026."
    )
