import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    auto_labels = state.get("autoLabels", [])

    # Find auto label "Legal" with criteria matching from legalwise.com
    legal_auto_label = None
    for al in auto_labels:
        if al.get("name") == "Legal":
            legal_auto_label = al
            break
    if not legal_auto_label:
        return False, "Auto label 'Legal' not found."

    criteria = legal_auto_label.get("criteria", {})
    criteria_from = criteria.get("from", "")
    if "legalwise.com" not in criteria_from.lower():
        return False, f"Auto label 'Legal' criteria.from is '{criteria_from}', expected to contain 'legalwise.com'."

    # Find auto label "Support Ticket" and check it's disabled
    support_ticket = None
    for al in auto_labels:
        if al.get("name") == "Support Ticket":
            support_ticket = al
            break
    if not support_ticket:
        return False, "Auto label 'Support Ticket' not found."
    if support_ticket.get("enabled") is not False:
        return False, f"Auto label 'Support Ticket' enabled is {support_ticket.get('enabled')}, expected false."

    return True, "Auto label 'Legal' created with legalwise.com criteria, 'Support Ticket' auto label disabled."
