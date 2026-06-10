import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Reply to Kevin Zhao (kevin.zhao@quantumlab.tech) about quantum computing
    # CC Ryan Cooper (ryan.cooper@saasplatform.io) who sent the SaaS Platform API email
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

        cc_emails = set()
        for r in e.get("cc", []):
            if isinstance(r, dict):
                cc_emails.add(r.get("email", ""))
            elif isinstance(r, str):
                cc_emails.add(r)

        if ("kevin.zhao@quantumlab.tech" in to_emails
                and "ryan.cooper@saasplatform.io" in cc_emails):
            subj = (e.get("subject") or "").lower()
            if "quantum" in subj or "prototype" in subj or "integration" in subj:
                found = e
                break

    if not found:
        return False, "No reply found to Kevin Zhao with Ryan Cooper on CC."

    return True, "Reply sent to Kevin Zhao with Ryan Cooper (SaaS Platform) on CC."
