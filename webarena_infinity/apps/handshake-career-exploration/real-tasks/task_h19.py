import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check 1: A salary negotiation appointment exists with the specified details
    appointments = state.get("appointments", [])
    found_appt = False
    for appt in appointments:
        if (
            appt.get("category") == "Networking & Professional Development"
            and appt.get("type") == "Salary Negotiation"
            and appt.get("date") == "2026-03-13"
            and appt.get("time") == "3:00 PM"
            and appt.get("medium") == "Phone"
            and appt.get("status") == "requested"
        ):
            found_appt = True
            break

    if not found_appt:
        appt_summaries = [
            {
                "id": a.get("id"),
                "category": a.get("category"),
                "type": a.get("type"),
                "date": a.get("date"),
                "time": a.get("time"),
                "medium": a.get("medium"),
                "status": a.get("status"),
            }
            for a in appointments
        ]
        errors.append(
            f"No appointment found matching: category='Networking & Professional Development', "
            f"type='Salary Negotiation', date='2026-03-13', time='3:00 PM', "
            f"medium='Phone', status='requested'. "
            f"Current appointments: {appt_summaries}"
        )

    # Check 2: Phone number updated
    phone = state.get("currentUser", {}).get("phone", "")
    if phone != "(650) 555-0200":
        errors.append(
            f"Phone number is '{phone}', expected '(650) 555-0200'."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Salary Negotiation appointment scheduled for 2026-03-13 at 3:00 PM by Phone, "
        "and phone number updated to '(650) 555-0200'."
    )
