# Task: Delete Design-company contacts, dismiss related merges, delete auto-saved from those domains.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    contacts = state.get("contacts", [])
    other_contacts = state.get("otherContacts", [])
    merges = state.get("mergeSuggestions", [])

    # Contacts from companies with 'Design' should be deleted
    deleted_contacts = [
        ("Marcus", "Williams", "DesignHub"),
        ("Sophie", "Laurent", "EuroDesign"),
        ("Elena", "Volkov", "EuroDesign"),
    ]
    for first, last, company in deleted_contacts:
        found = any(
            c.get("firstName") == first and c.get("lastName") == last
            for c in contacts
        )
        if found:
            errors.append(f"{first} {last} ({company}) should be deleted")

    # merge_2 (EuroDesign) should be dismissed
    merge2 = None
    for m in merges:
        if m.get("id") == "merge_2":
            merge2 = m
            break
    if merge2 is None:
        errors.append("merge_2 not found")
    elif not merge2.get("dismissed"):
        errors.append("EuroDesign merge suggestion should be dismissed")

    # Auto-saved contacts from Design domains should be deleted
    design_domains = ["designhub.com", "eurodesign.fr"]
    for oc in other_contacts:
        email = oc.get("email", "")
        for domain in design_domains:
            if email.endswith(f"@{domain}"):
                errors.append(
                    f"Auto-saved contact '{email}' should be deleted "
                    f"(from Design company domain)"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Design company contacts, related merges, and auto-saved contacts cleaned up."
