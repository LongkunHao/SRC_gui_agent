import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Design Review on 2026-03-08 attendees: marcus.w@designhub.io, maya.patel@acmecorp.com
    # Acme Corp attendee = maya.patel@acmecorp.com
    # Check for a forwarded email to Maya
    forwarded = None
    for e in state.get("emails", []):
        if e["from"]["email"] == "alex.morgan@acmecorp.com":
            to_emails = set()
            for r in e.get("to", []):
                if isinstance(r, dict):
                    to_emails.add(r.get("email", ""))
                elif isinstance(r, str):
                    to_emails.add(r)
            if "maya.patel@acmecorp.com" in to_emails:
                subj = (e.get("subject") or "").lower()
                if "brand" in subj or "assets" in subj:
                    forwarded = e
                    break

    if not forwarded:
        return False, "No forwarded email about brand assets found to maya.patel@acmecorp.com."

    # Check it looks like a forward (subject contains Fwd or forward)
    subj = forwarded.get("subject", "")
    if "fwd" not in subj.lower() and "forward" not in subj.lower():
        return False, f"Email subject '{subj}' doesn't appear to be a forward."

    return True, "Brand assets email forwarded to Acme Corp Design Review attendee (Maya Patel)."
