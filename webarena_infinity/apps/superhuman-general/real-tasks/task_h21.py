import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find a sent reply to Michael Foster about CloudScale with CC to James O'Brien
    for e in state.get("emails", []):
        from_email = e.get("from", {}).get("email", "")
        if from_email != "alex.morgan@acmecorp.com":
            continue
        if e.get("isDraft", False):
            continue

        # Check recipient includes michael.f@cloudscale.dev
        to_emails = []
        for r in e.get("to", []):
            if isinstance(r, dict):
                to_emails.append(r.get("email", ""))
            elif isinstance(r, str):
                to_emails.append(r)
        if "michael.f@cloudscale.dev" not in to_emails:
            continue

        # Check CC includes james.obrien@legalwise.com
        cc_emails = []
        for r in e.get("cc", []):
            if isinstance(r, dict):
                cc_emails.append(r.get("email", ""))
            elif isinstance(r, str):
                cc_emails.append(r)
        if "james.obrien@legalwise.com" not in cc_emails:
            continue

        # Check subject relates to CloudScale
        subject = (e.get("subject") or "").lower()
        if "cloudscale" in subject or "contract" in subject:
            return True, f"Found reply to Michael Foster with CC James O'Brien. Subject: {e.get('subject')}"

    return False, "Could not find a sent reply to michael.f@cloudscale.dev with CC james.obrien@legalwise.com about CloudScale."
