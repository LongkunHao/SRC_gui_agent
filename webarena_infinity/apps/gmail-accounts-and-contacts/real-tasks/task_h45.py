# Task: Delete automated service other-contacts, move person with fewest interactions.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    other_contacts = state.get("otherContacts", [])
    contacts = state.get("contacts", [])

    # Automated service emails (no firstName) that should be deleted
    service_emails = {
        "support@vercel.com", "billing@aws.amazon.com", "hr@techcorp.io",
        "no-reply@stripe.com", "noreply@github.com", "receipts@uber.com",
        "team@linear.app", "do-not-reply@zoom.us", "alerts@datadog.com",
        "notifications@jira.atlassian.com", "newsletter@hackernews.com",
        "no-reply@docusign.net",
    }
    for oc in other_contacts:
        if oc.get("email") in service_emails:
            errors.append(
                f"Auto-saved service contact '{oc.get('email')}' should have been deleted"
            )

    # Chloe Bennett (fewest interactions = 1) should be moved to main contacts
    chloe_in_other = any(
        oc.get("email") == "chloe.b@sequoiacap.com" for oc in other_contacts
    )
    if chloe_in_other:
        errors.append("Chloe Bennett should have been moved out of other contacts")

    chloe_in_main = any(
        c.get("email") == "chloe.b@sequoiacap.com" for c in contacts
    )
    if not chloe_in_main:
        errors.append("Chloe Bennett should be in main contacts")

    # Real people who should still be in other contacts
    remaining_people = [
        "jason.blake@salesforce.com", "tina.marshall@designhub.com",
        "alex.rivera@notion.so", "mike.santos@cloudflare.com",
        "wendy.chung@techcorp.io", "peter.grant@mongodb.com",
        "nina.k@figma.com",
    ]
    for email in remaining_people:
        found = any(oc.get("email") == email for oc in other_contacts)
        if not found:
            errors.append(f"Real person '{email}' should still be in other contacts")

    if errors:
        return False, "; ".join(errors)
    return True, "Service contacts deleted, Chloe Bennett moved to main contacts."
