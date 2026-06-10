# Task: Find best friend from college's company, delete auto-saved contacts from that company.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Best friend from college = Jake Morrison, company = Stripe
    # Auto-saved from Stripe: no-reply@stripe.com (Stripe Notifications)
    other_contacts = state.get("otherContacts", [])
    for oc in other_contacts:
        if oc.get("email") == "no-reply@stripe.com":
            errors.append("Stripe Notifications (no-reply@stripe.com) should be deleted")
            break

    if errors:
        return False, "; ".join(errors)
    return True, "Auto-saved Stripe contact deleted."
