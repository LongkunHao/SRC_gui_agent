import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find a sent email to Sophie Laurent at sophie.l@eurodesign.fr
    sent_email = None
    for e in state.get("emails", []):
        # Check if this is a sent email from alex.morgan
        from_email = e.get("from", {}).get("email", "")
        if "alex.morgan" not in from_email:
            continue

        # Check if addressed to sophie.l@eurodesign.fr
        to_list = e.get("to", [])
        to_emails = []
        for recipient in to_list:
            if isinstance(recipient, dict):
                to_emails.append(recipient.get("email", ""))
            elif isinstance(recipient, str):
                to_emails.append(recipient)

        if any("sophie" in addr.lower() and "eurodesign" in addr.lower() for addr in to_emails):
            sent_email = e
            break

    if not sent_email:
        return False, "No sent email to Sophie Laurent (sophie.l@eurodesign.fr) found."

    # Check it's not a draft
    if sent_email.get("isDraft", False):
        return False, "Email to Sophie Laurent is still a draft, not sent."

    # Check subject or body references acceptance/speaking/EuroDesign
    subject = sent_email.get("subject", "").lower()
    body = sent_email.get("body", "").lower()
    combined = subject + " " + body

    acceptance_keywords = ["accept", "confirm", "happy to", "pleased to", "look forward", "eurodesign", "speaking", "invitation", "attend"]
    if not any(kw in combined for kw in acceptance_keywords):
        return False, f"Email to Sophie does not appear to reference acceptance of the speaking invitation. Subject: '{sent_email.get('subject', '')}'"

    return True, "Email sent to Sophie Laurent accepting the EuroDesign speaking invitation."
