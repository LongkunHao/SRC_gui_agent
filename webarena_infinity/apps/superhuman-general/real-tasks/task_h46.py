import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Most recent in Recent Opens: Emily Rodriguez read email 69 at 2026-03-07T08:30
    # Emily's inbox email: id 2 "Re: Series B Term Sheet Discussion"
    # Check for a reply to Emily

    found = None
    for e in state.get("emails", []):
        if e["from"]["email"] != "alex.morgan@acmecorp.com":
            continue
        if e.get("isDraft"):
            continue

        to_emails = set()
        for r in e.get("to", []):
            if isinstance(r, dict):
                to_emails.add(r.get("email", ""))
            elif isinstance(r, str):
                to_emails.add(r)

        if "emily.r@venturelabs.co" in to_emails:
            subj = (e.get("subject") or "").lower()
            # Check it's a reply to the term sheet email
            if "term sheet" in subj or "series b" in subj:
                found = e
                break

    if not found:
        return False, "No reply found to Emily Rodriguez's term sheet email."

    return True, "Reply sent to Emily Rodriguez (discovered via most recent read receipt in Recent Opens)."
