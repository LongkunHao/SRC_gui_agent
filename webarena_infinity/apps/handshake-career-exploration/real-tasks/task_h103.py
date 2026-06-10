"""
Task: Your only approved upcoming appointment is with a career counselor.
Schedule a Professional Branding appointment with that same counselor for
March 18, 2026 at 2:00 PM, virtually.

Discovery: appt_01 is the only approved upcoming appointment, with
Michael Okafor (staff_06).

Verify:
(1) New appointment: type="Professional Branding",
    staffId="staff_06" OR staffName="Michael Okafor",
    date="2026-03-18", time="2:00 PM", medium="Virtual on Handshake"
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    appointments = state.get("appointments", [])

    matching = [
        a for a in appointments
        if a.get("id") != "appt_01"
        and "Professional Branding" in a.get("type", "")
        and a.get("date") == "2026-03-18"
        and a.get("time") == "2:00 PM"
        and "virtual" in a.get("medium", "").lower()
    ]

    if not matching:
        return False, (
            "No Professional Branding appointment found for March 18 at 2:00 PM virtually."
        )

    appt = matching[0]
    if appt.get("staffId") != "staff_06" and "Michael Okafor" not in appt.get("staffName", ""):
        return False, (
            f"Appointment not with Michael Okafor (staff_06). "
            f"Got staffId='{appt.get('staffId')}', staffName='{appt.get('staffName')}'."
        )

    return True, (
        "Professional Branding appointment scheduled with Michael Okafor "
        "(discovered from approved appointment) for March 18 at 2:00 PM virtually."
    )
