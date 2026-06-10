import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find a sent email to David Kim about partnership/scheduling/call
    target_email = None
    for e in state.get("emails", []):
        # Check if it's sent by the user (alex.morgan@acmecorp.com)
        from_email = e.get("from", {}).get("email", "")
        if from_email != "alex.morgan@acmecorp.com":
            continue

        # Check it's not a draft
        if e.get("isDraft", False):
            continue

        # Check recipient includes david.kim@financeplus.com
        recipients = e.get("to", [])
        has_david = False
        for r in recipients:
            if isinstance(r, dict):
                if r.get("email") == "david.kim@financeplus.com":
                    has_david = True
                    break
            elif isinstance(r, str):
                if r == "david.kim@financeplus.com":
                    has_david = True
                    break
        if not has_david:
            continue

        # Check subject or body mentions partnership, scheduling, or call
        subject = (e.get("subject") or "").lower()
        body = (e.get("body") or "").lower()
        combined = subject + " " + body
        keywords = ["partnership", "scheduling", "call", "schedule", "partner"]
        if any(kw in combined for kw in keywords):
            target_email = e
            break

    if not target_email:
        return False, "Could not find a sent (non-draft) email from alex.morgan@acmecorp.com to david.kim@financeplus.com mentioning partnership/scheduling/call."

    return True, f"Found sent email to David Kim about partnership/scheduling. Subject: {target_email.get('subject')}"
