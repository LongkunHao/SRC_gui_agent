import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Quarterly OKR Review organizer: priya.sharma@acmecorp.com
    # Other attendees: sarah.chen@acmecorp.com, patrick.oneil@acmecorp.com
    # (Priya is also in attendees but she's the organizer/recipient)

    # Find a sent email to Priya about OKR/Q2
    sent = None
    for e in state.get("emails", []):
        if (e["from"]["email"] == "alex.morgan@acmecorp.com"
                and not e.get("isDraft")):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "priya.sharma@acmecorp.com" in to_emails:
                subj = e.get("subject", "").lower()
                if "okr" in subj or "q2" in subj or "objective" in subj:
                    sent = e
                    break

    if not sent:
        return False, "No sent email found to Priya Sharma about OKR/Q2 objectives."

    # Check CC includes Sarah Chen and Patrick O'Neil
    cc_emails = {r["email"] for r in sent.get("cc", [])}
    required_cc = {"sarah.chen@acmecorp.com", "patrick.oneil@acmecorp.com"}
    missing = required_cc - cc_emails
    if missing:
        return False, f"Missing CC recipients: {', '.join(missing)}"

    return True, "Email sent to OKR Review organizer with correct CC recipients."
