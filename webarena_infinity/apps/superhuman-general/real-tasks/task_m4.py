import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the email "Quantum Computing Integration Prototype" from "Kevin Zhao"
    target_email = None
    for e in state.get("emails", []):
        if (e.get("subject") == "Quantum Computing Integration Prototype"
                and e.get("from", {}).get("name") == "Kevin Zhao"):
            target_email = e
            break
    if not target_email:
        return False, "Could not find email 'Quantum Computing Integration Prototype' from Kevin Zhao."

    # Check that remindAt is set and contains the date for next Monday (March 9, 2026)
    remind_at = target_email.get("remindAt")
    if not remind_at:
        return False, "Email does not have a reminder set (remindAt is not set)."

    if "2026-03-09" in str(remind_at):
        return True, f"Reminder has been set for next Monday (March 9, 2026). remindAt: {remind_at}"
    else:
        return False, f"Reminder is set but not for March 9, 2026. remindAt: {remind_at}"
