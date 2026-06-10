import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Board Meeting Prep (evt_4, March 7): attendees are priya.sharma and ben.carter
    # Organizer: alex.morgan (us). So the "other attendee" besides Priya = Ben Carter
    # Reply to budget email (from Priya), CC Ben

    found = None
    for e in state.get("emails", []):
        if (e["from"]["email"] == "alex.morgan@acmecorp.com"
                and not e.get("isDraft")):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "priya.sharma@acmecorp.com" in to_emails:
                subj = e.get("subject", "").lower()
                if "budget" in subj:
                    found = e
                    break

    if not found:
        return False, "No reply to Priya's budget email found."

    cc_emails = {r["email"] for r in found.get("cc", [])}
    if "ben.carter@acmecorp.com" not in cc_emails:
        return False, f"Ben Carter not in CC. CC has: {', '.join(cc_emails)}"

    return True, "Reply to budget email sent with Board Meeting Prep co-attendee on CC."
