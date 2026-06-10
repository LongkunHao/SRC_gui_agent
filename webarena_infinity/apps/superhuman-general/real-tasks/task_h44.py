import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Q1 Board Meeting attendees: emily.r@venturelabs.co, lena.j@nordicventures.se,
    # priya.sharma@acmecorp.com, patrick.oneil@acmecorp.com
    # External = emily.r@venturelabs.co, lena.j@nordicventures.se
    # CC = patrick.oneil@acmecorp.com

    required_to = {"emily.r@venturelabs.co", "lena.j@nordicventures.se"}
    required_cc = {"patrick.oneil@acmecorp.com"}

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

        if not required_to.issubset(to_emails):
            continue

        cc_emails = set()
        for r in e.get("cc", []):
            if isinstance(r, dict):
                cc_emails.add(r.get("email", ""))
            elif isinstance(r, str):
                cc_emails.add(r)

        if not required_cc.issubset(cc_emails):
            continue

        # Check subject/body references board or follow-up
        text = ((e.get("subject") or "") + " " + (e.get("body") or "")).lower()
        if "board" in text or "follow" in text or "meeting" in text:
            found = e
            break

    if not found:
        return False, "No sent email found to external Board Meeting attendees with Patrick on CC."

    return True, "Email sent to external Q1 Board Meeting attendees with Patrick O'Neil on CC."
