import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Inbox emails with read receipts:
    # email 3 (David Kim, FinancePlus): openCount 2
    # email 6 (Kevin Zhao, QuantumLab): openCount 3  ← highest
    # The one with the highest open count is Kevin Zhao's quantum computing email

    clients_id = None
    for label in state.get("labels", []):
        if label["name"] == "Clients":
            clients_id = label["id"]
            break
    if not clients_id:
        return False, "Clients label not found."

    target = None
    for e in state.get("emails", []):
        if (e["subject"] == "Quantum Computing Integration Prototype"
                and e["from"]["email"] == "kevin.zhao@quantumlab.tech"):
            target = e
            break

    if not target:
        return False, "Kevin Zhao's quantum computing email not found."

    if clients_id not in target.get("labels", []):
        return False, "Kevin Zhao's email (highest open count) does not have the 'Clients' label."

    return True, "'Clients' label added to the email with the highest read receipt open count."
