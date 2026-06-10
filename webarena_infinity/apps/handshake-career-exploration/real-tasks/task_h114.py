"""
Task: Create a feed post for everyone about the value of informational
interviews, then schedule a networking strategy appointment with the finance
and consulting specialist for March 20, 2026 at 2:00 PM, virtually.

Discovery: Finance/Consulting specialist: James Chen (staff_02).
March 20 has staff_02 available at 2:00 PM.

Verify:
(1) New post from Maya with audience="everyone" mentioning "informational"
(2) New appointment: type="Networking Strategy", staffId="staff_02" OR
    staffName="James Chen", date="2026-03-20", time="2:00 PM",
    medium="Virtual on Handshake"
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: New post about informational interviews
    posts = state.get("feedPosts", [])
    found_post = any(
        "Maya" in p.get("authorName", "")
        and p.get("audience") == "everyone"
        and "informational" in p.get("content", "").lower()
        for p in posts
    )
    if not found_post:
        errors.append(
            "No post from Maya with audience='everyone' mentioning 'informational'."
        )

    # Check 2: Networking Strategy appointment with James Chen
    appointments = state.get("appointments", [])
    matching = [
        a for a in appointments
        if a.get("type") == "Networking Strategy"
        and a.get("date") == "2026-03-20"
        and a.get("time") == "2:00 PM"
        and "virtual" in a.get("medium", "").lower()
    ]
    if not matching:
        errors.append(
            "No Networking Strategy appointment for March 20 at 2:00 PM virtually."
        )
    else:
        appt = matching[0]
        if appt.get("staffId") != "staff_02" and "James Chen" not in appt.get("staffName", ""):
            errors.append(
                f"Appointment not with James Chen. Got staffId='{appt.get('staffId')}'"
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Post about informational interviews created. "
        "Networking Strategy appointment scheduled with James Chen."
    )
