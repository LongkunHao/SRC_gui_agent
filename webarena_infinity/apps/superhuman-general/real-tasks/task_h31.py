import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # 1. Check forwarded email exists (sent from Alex to Sarah about EuroDesign)
    forwarded = False
    for e in state.get("emails", []):
        from_email = e.get("from", {}).get("email", "")
        if from_email != "alex.morgan@acmecorp.com":
            continue
        if e.get("isDraft", False):
            continue

        to_emails = []
        for r in e.get("to", []):
            if isinstance(r, dict):
                to_emails.append(r.get("email", ""))
            elif isinstance(r, str):
                to_emails.append(r)
        if "sarah.chen@acmecorp.com" not in to_emails:
            continue

        subject = (e.get("subject") or "").lower()
        body = (e.get("body") or "").lower()
        combined = subject + " " + body
        if "eurodesign" in combined or "conference" in combined or "speaker" in combined:
            forwarded = True
            break

    if not forwarded:
        return False, "Could not find a forwarded email from Alex to sarah.chen@acmecorp.com about EuroDesign."

    # 2. Check original Sophie Laurent invitation has 'Work' label
    work_label = None
    for label in state.get("labels", []):
        if label["name"] == "Work":
            work_label = label
            break
    if not work_label:
        return False, "Label 'Work' not found."
    work_id = work_label["id"]

    original = None
    for e in state.get("emails", []):
        if (e["subject"] == "EuroDesign Conference - Speaker Invitation"
                and e["from"]["email"] == "sophie.l@eurodesign.fr"):
            original = e
            break
    if not original:
        return False, "Original EuroDesign invitation from Sophie Laurent not found."

    if work_id not in original.get("labels", []):
        return False, f"Original EuroDesign invitation does not have 'Work' label (labels: {original.get('labels', [])})."

    return True, "EuroDesign invitation forwarded to Sarah Chen and 'Work' label added to original email."
