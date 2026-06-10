import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    finance_label = None
    clients_label = None
    for label in state.get("labels", []):
        if label["name"] == "Finance":
            finance_label = label
        elif label["name"] == "Clients":
            clients_label = label
    if not finance_label:
        return False, "Label 'Finance' not found."
    if not clients_label:
        return False, "Label 'Clients' not found."

    fin_id = finance_label["id"]
    cli_id = clients_label["id"]

    acme_domain = "acmecorp.com"
    errors = []

    for e in state.get("emails", []):
        # Only inbox Important split with attachments
        if (not e.get("hasAttachments")
                or e.get("splitCategory") != "important"
                or e.get("isDone") or e.get("isTrashed")
                or e.get("isSpam") or e.get("isDraft")
                or e.get("remindAt") is not None):
            continue

        sender = e["from"]["email"]
        labels = e.get("labels", [])

        if sender.endswith("@" + acme_domain):
            # Acme sender → should have Finance label
            if fin_id not in labels:
                errors.append(f"Acme email '{e['subject']}' missing 'Finance' label.")
        else:
            # External sender → should have Clients label
            if cli_id not in labels:
                errors.append(f"External email '{e['subject']}' missing 'Clients' label.")

    if errors:
        return False, " ".join(errors)

    return True, "Finance label added to Acme attachment emails; Clients label added to external attachment emails."
