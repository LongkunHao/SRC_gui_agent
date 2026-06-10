import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointments = state.get("appointments", [])

    # Look for a new appointment matching the criteria
    for appt in appointments:
        category = appt.get("category", "")
        appt_type = appt.get("type", "")
        date = appt.get("date", "")
        time = appt.get("time", "")
        medium = appt.get("medium", "")
        status = appt.get("status", "")

        if (
            category == "Networking & Professional Development"
            and appt_type == "Networking Strategy"
            and date == "2026-03-17"
            and time == "1:00 PM"
            and medium == "Virtual on Handshake"
            and status == "requested"
        ):
            return True, (
                f"Found matching networking strategy appointment: "
                f"date={date}, time={time}, medium={medium}, status={status}"
            )

    # Provide diagnostic info about existing appointments
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
    return False, (
        f"No appointment found matching: category='Networking & Professional Development', "
        f"type='Networking Strategy', date='2026-03-17', time='1:00 PM', "
        f"medium='Virtual on Handshake', status='requested'. "
        f"Current appointments: {appt_summaries}"
    )
