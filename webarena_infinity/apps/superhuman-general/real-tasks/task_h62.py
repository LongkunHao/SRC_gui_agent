import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Work label ID
    work_id = None
    for label in state.get("labels", []):
        if label["name"] == "Work":
            work_id = label["id"]
            break
    if not work_id:
        return False, "Work label not found."

    # Originally-unread inbox emails with attachments → must be starred
    attach_emails = [
        ("Q2 Product Roadmap - Final Review", "sarah.chen@acmecorp.com"),
        ("Budget Approval Needed - Marketing Campaign", "priya.sharma@acmecorp.com"),
    ]

    # Originally-unread inbox emails without attachments → must have Work label
    no_attach_emails = [
        ("Re: Series B Term Sheet Discussion", "emily.r@venturelabs.co"),
        ("Partnership Opportunity - FinancePlus x Acme", "david.kim@financeplus.com"),
        ("[acme/platform] PR #1842 merged: Add real-time collaboration", "notifications@github.com"),
        ("[acme/platform] Issue #923: Memory leak in WebSocket handler", "notifications@github.com"),
        ("Today's Briefing: AI Startup Funding Hits Record $12B in Q1", "newsletter@theinformation.com"),
        ("Database Performance Report - March", "tom.bradley@acmecorp.com"),
        ("Accessibility Audit Results", "maya.patel@acmecorp.com"),
        ("Deploy failed: acme-marketing-site", "team@netlify.com"),
    ]

    errors = []

    for subj, sender in attach_emails:
        for e in state["emails"]:
            if e["subject"] == subj and e["from"]["email"] == sender:
                if not e.get("isStarred"):
                    errors.append(f"'{subj}' (has attachment) is not starred.")
                break

    for subj, sender in no_attach_emails:
        for e in state["emails"]:
            if e["subject"] == subj and e["from"]["email"] == sender:
                if work_id not in e.get("labels", []):
                    errors.append(f"'{subj}' (no attachment) missing 'Work' label.")
                break

    if errors:
        return False, " ".join(errors)

    return True, "All unread inbox emails correctly starred (with attachments) or labeled 'Work' (without)."
