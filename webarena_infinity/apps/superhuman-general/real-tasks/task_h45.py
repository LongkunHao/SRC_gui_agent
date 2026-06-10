import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # The snoozed email about payment terms is from david.kim@financeplus.com
    # David Kim's inbox email is "Partnership Opportunity - FinancePlus x Acme"
    email = None
    for e in state.get("emails", []):
        if (e["subject"] == "Partnership Opportunity - FinancePlus x Acme"
                and e["from"]["email"] == "david.kim@financeplus.com"):
            email = e
            break

    if not email:
        return False, "Could not find 'Partnership Opportunity - FinancePlus x Acme' email."

    if not email.get("isDone"):
        return False, "Email is not archived (isDone is not true)."

    return True, "David Kim's partnership email archived (discovered via payment terms reminder)."
