"""
Task: You have two requested appointments. Cancel the one scheduled further
in the future, and add a comment to the earlier one asking to discuss
interview frameworks.

Discovery: Requested appointments:
  appt_02 (March 21 - Mock Interview Technical with David Kim)
  appt_08 (March 28 - Case Interview Prep with James Chen)
Further: appt_08 → cancel. Earlier: appt_02 → add comment.

Verify:
(1) appt_08 status == "cancelled"
(2) appt_02 has new comment from Maya mentioning "framework" (case-insensitive)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    appointments = state.get("appointments", [])

    # Check 1: appt_08 cancelled
    appt_08 = next((a for a in appointments if a.get("id") == "appt_08"), None)
    if appt_08 is None:
        errors.append("appt_08 not found.")
    elif appt_08.get("status") != "cancelled":
        errors.append(
            f"appt_08 not cancelled. status='{appt_08.get('status')}'"
        )

    # Check 2: appt_02 has comment about frameworks
    appt_02 = next((a for a in appointments if a.get("id") == "appt_02"), None)
    if appt_02 is None:
        errors.append("appt_02 not found.")
    else:
        found = any(
            "maya" in c.get("author", "").lower()
            and "framework" in c.get("text", "").lower()
            for c in appt_02.get("comments", [])
        )
        if not found:
            errors.append(
                "No comment from Maya mentioning 'framework' on appt_02."
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Later appointment (appt_08) cancelled. "
        "Comment about interview frameworks added to earlier appointment (appt_02)."
    )
