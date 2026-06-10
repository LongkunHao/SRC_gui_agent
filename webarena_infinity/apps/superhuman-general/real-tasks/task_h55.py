import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    sophie_sent = None
    biomed_draft_exists = False

    for e in state.get("emails", []):
        # Check for sent (non-draft) email to Sophie about EuroDesign
        if e["from"]["email"] == "alex.morgan@acmecorp.com":
            to_emails = set()
            for r in e.get("to", []):
                if isinstance(r, dict):
                    to_emails.add(r.get("email", ""))
                elif isinstance(r, str):
                    to_emails.add(r)

            if "sophie.l@eurodesign.fr" in to_emails:
                subj = (e.get("subject") or "").lower()
                if "eurodesign" in subj or "speaker" in subj or "conference" in subj:
                    if not e.get("isDraft"):
                        sophie_sent = e

            if "jennifer.wu@biomedresearch.com" in to_emails:
                subj = (e.get("subject") or "").lower()
                if ("biomed" in subj or "proposal" in subj or "research" in subj
                        or "collaboration" in subj):
                    if e.get("isDraft"):
                        biomed_draft_exists = True

    errors = []
    if not sophie_sent:
        return False, "No sent (non-draft) email found to Sophie Laurent about the EuroDesign conference."
    if biomed_draft_exists:
        errors.append("BioMed proposal draft still exists (should have been deleted).")

    if errors:
        return False, " ".join(errors)

    return True, "EuroDesign draft sent to Sophie Laurent; BioMed proposal draft deleted."
