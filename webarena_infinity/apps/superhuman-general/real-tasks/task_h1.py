import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Clients" label
    clients_label = None
    for label in state.get("labels", []):
        if label["name"] == "Clients":
            clients_label = label
            break
    if not clients_label:
        return False, "Label 'Clients' not found."
    clients_id = clients_label["id"]

    # Find "Partnership Opportunity - FinancePlus x Acme" from "David Kim"
    partnership_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Partnership Opportunity - FinancePlus x Acme" and e["from"]["name"] == "David Kim":
            partnership_email = e
            break
    if not partnership_email:
        return False, "Could not find 'Partnership Opportunity - FinancePlus x Acme' email from David Kim."

    # Find "Quantum Computing Integration Prototype" from "Kevin Zhao"
    quantum_email = None
    for e in state.get("emails", []):
        if e["subject"] == "Quantum Computing Integration Prototype" and e["from"]["name"] == "Kevin Zhao":
            quantum_email = e
            break
    if not quantum_email:
        return False, "Could not find 'Quantum Computing Integration Prototype' email from Kevin Zhao."

    # Check both emails have the Clients label
    if clients_id not in partnership_email.get("labels", []):
        return False, f"Partnership email does not have the 'Clients' label (expected '{clients_id}' in {partnership_email.get('labels', [])})."
    if clients_id not in quantum_email.get("labels", []):
        return False, f"Quantum Computing email does not have the 'Clients' label (expected '{clients_id}' in {quantum_email.get('labels', [])})."

    return True, "Both emails have the 'Clients' label applied."
