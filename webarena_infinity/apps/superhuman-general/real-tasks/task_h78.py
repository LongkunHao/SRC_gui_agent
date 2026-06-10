import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # 1. Draft reply to Sophie (about EuroDesign) should be sent (isDraft: false)
    draft_sent = False
    for e in state.get("emails", []):
        if (e["from"]["email"] == "alex.morgan@acmecorp.com"
                and not e.get("isDraft")
                and "EuroDesign" in e.get("subject", "")):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "sophie.l@eurodesign.fr" in to_emails:
                draft_sent = True
                break

    if not draft_sent:
        # Check if draft still exists
        for e in state.get("emails", []):
            if (e.get("isDraft") and "EuroDesign" in e.get("subject", "")):
                errors.append("Sophie's EuroDesign draft is still a draft (not sent).")
                break
        else:
            errors.append("Sophie's EuroDesign email not found (neither sent nor draft).")

    # 2. Forwarded EuroDesign invitation to Patrick O'Neil (Q1 Board Meeting organizer)
    fwd_found = False
    for e in state.get("emails", []):
        if (e["from"]["email"] == "alex.morgan@acmecorp.com"
                and not e.get("isDraft")):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "patrick.oneil@acmecorp.com" in to_emails:
                subj = e.get("subject", "").lower()
                if "eurodesign" in subj and ("fwd" in subj or "forward" in subj):
                    fwd_found = True
                    break

    if not fwd_found:
        errors.append("No forwarded EuroDesign invitation to Patrick O'Neil found.")

    if errors:
        return False, " ".join(errors)

    return True, "EuroDesign draft sent and original invitation forwarded to Q1 Board Meeting organizer."
