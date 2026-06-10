import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointments = state.get("appointments", [])
    appt_01 = next((a for a in appointments if a.get("id") == "appt_01"), None)
    if appt_01 is None:
        return False, "Appointment appt_01 not found in state."

    comments = appt_01.get("comments", [])
    # Seed data has 1 comment from Michael Okafor. Look for a new comment from Maya Chen mentioning LinkedIn.
    for comment in comments:
        author = comment.get("author", "")
        text = comment.get("text", "").lower()
        if "maya" in author.lower() and "linkedin" in text:
            return True, f"Found comment from Maya Chen mentioning LinkedIn: '{comment.get('text')}'"

    return False, (
        f"No comment from Maya Chen containing 'LinkedIn' found on appt_01. "
        f"Current comments: {[{'author': c.get('author'), 'text': c.get('text', '')[:80]} for c in comments]}"
    )
