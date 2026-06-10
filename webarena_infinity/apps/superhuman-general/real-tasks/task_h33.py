import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state.get("emails", []):
        from_email = e.get("from", {}).get("email", "")
        if from_email != "alex.morgan@acmecorp.com":
            continue
        if e.get("isDraft", False):
            continue

        # Check To includes Kevin Zhao and Ryan Cooper
        to_emails = set()
        for r in e.get("to", []):
            if isinstance(r, dict):
                to_emails.add(r.get("email", ""))
            elif isinstance(r, str):
                to_emails.add(r)

        if not {"kevin.zhao@quantumlab.tech", "ryan.cooper@saasplatform.io"}.issubset(to_emails):
            continue

        # Check CC includes Sarah Chen
        cc_emails = set()
        for r in e.get("cc", []):
            if isinstance(r, dict):
                cc_emails.add(r.get("email", ""))
            elif isinstance(r, str):
                cc_emails.add(r)

        if "sarah.chen@acmecorp.com" not in cc_emails:
            continue

        # Check subject/body mentions API or integration
        subject = (e.get("subject") or "").lower()
        body = (e.get("body") or "").lower()
        combined = subject + " " + body
        if "api" in combined or "integration" in combined:
            return True, f"Found email to Kevin Zhao and Ryan Cooper with CC Sarah Chen. Subject: {e.get('subject')}"

    return False, "Could not find a sent email to kevin.zhao@quantumlab.tech and ryan.cooper@saasplatform.io with CC sarah.chen@acmecorp.com about API integration."
