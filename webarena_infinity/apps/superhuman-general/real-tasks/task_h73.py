import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    urgent_id = None
    for label in state.get("labels", []):
        if label["name"] == "Urgent":
            urgent_id = label["id"]
            break
    if not urgent_id:
        return False, "Urgent label not found."

    errors = []
    archived_count = 0

    for e in state.get("emails", []):
        # Only check Important split inbox emails that were originally read
        if (e.get("splitCategory") == "important"
                and not e.get("isTrashed")
                and not e.get("isSpam")
                and not e.get("isDraft")):

            # We need to identify emails that SHOULD have been archived:
            # originally read + important inbox + not starred + not Urgent
            # The agent may have marked some as done. We check:
            # - If email was originally starred → should NOT be archived
            # - If email had Urgent label → should NOT be archived
            # - If email was originally unread → should NOT be archived

            # Use known seed data: unread emails were 1, 2, 3, 5, 113, 114
            # Starred emails: none in important inbox by default
            # Urgent label: email 2 (label_5)
            pass

    # Check specific originally-read important inbox emails are now archived
    # (Exclude: unread emails 1, 2, 3, 5, 113, 114; Urgent-labeled email 2)
    should_archive_subjects = [
        ("Re: Infrastructure Migration Plan", "tom.bradley@acmecorp.com"),
        ("Quantum Computing Integration Prototype", "kevin.zhao@quantumlab.tech"),
        ("Re: Sprint 23 Retrospective Notes", "nate.patel@acmecorp.com"),
        ("Design System Update - New Components Ready", "maya.patel@acmecorp.com"),
        ("Re: Engineering Manager Candidates", "rachel.foster@acmecorp.com"),
        ("New Brand Assets - Review Needed", "marcus.w@designhub.io"),
        ("Global Health Initiative - Sponsorship Request", "ana.g@globalhealth.org"),
        ("Executive Team Dinner - March 14", "patrick.oneil@acmecorp.com"),
        ("Re: Vendor Agreement - CloudScale", "james.obrien@legalwise.com"),
        ("Exclusive: Acme Feature in TechTrends Weekly", "michelle.park@mediaco.tv"),
        ("Office Lease Renewal - Decision Needed", "ben.carter@acmecorp.com"),
        ("Research Collaboration Proposal", "jennifer.wu@biomedresearch.com"),
        ("SaaS Platform Integration - API Access", "ryan.cooper@saasplatform.io"),
        ("Q1 Marketing Report - Outstanding Results", "diana.r@marketingpro.co"),
        ("EuroDesign Conference - Speaker Invitation", "sophie.l@eurodesign.fr"),
        ("Guest Lecture Request - Stanford CS Department", "robert.singh@university.edu"),
        ("CloudScale Contract - Ready to Sign", "michael.f@cloudscale.dev"),
        ("Creative Brief - Website Redesign", "lisa.n@creativeagency.co"),
        ("Nordic Ventures - Follow-up from Board Introduction", "lena.j@nordicventures.se"),
        ("Logistics Update - Office Equipment Delivery", "carlos.m@logisticspro.net"),
        ("Vendor Security Assessment - Q1 Results", "ben.carter@acmecorp.com"),
        ("Feature Flag Cleanup Proposal", "nate.patel@acmecorp.com"),
        ("New Employee Onboarding - Week of March 24", "rachel.foster@acmecorp.com"),
    ]

    should_not_archive = [
        # Unread emails - should stay in inbox
        ("Q2 Product Roadmap - Final Review", "sarah.chen@acmecorp.com"),
        ("Budget Approval Needed - Marketing Campaign", "priya.sharma@acmecorp.com"),
        ("Database Performance Report - March", "tom.bradley@acmecorp.com"),
        ("Accessibility Audit Results", "maya.patel@acmecorp.com"),
        # Urgent label
        ("Re: Series B Term Sheet Discussion", "emily.r@venturelabs.co"),
        # Also unread
        ("Partnership Opportunity - FinancePlus x Acme", "david.kim@financeplus.com"),
    ]

    for subj, sender in should_archive_subjects:
        for e in state["emails"]:
            if e["subject"] == subj and e["from"]["email"] == sender:
                if not e.get("isDone"):
                    errors.append(f"'{subj}' should be archived but isn't.")
                else:
                    archived_count += 1
                break

    for subj, sender in should_not_archive:
        for e in state["emails"]:
            if e["subject"] == subj and e["from"]["email"] == sender:
                if e.get("isDone"):
                    errors.append(f"'{subj}' should NOT be archived (unread or Urgent).")
                break

    if errors:
        return False, " ".join(errors[:3])

    if archived_count == 0:
        return False, "No read important inbox emails were archived."

    return True, f"{archived_count} read important inbox emails archived (unread and Urgent excluded)."
