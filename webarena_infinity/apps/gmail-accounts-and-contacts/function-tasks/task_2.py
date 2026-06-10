import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if (contact.get("firstName") == "Bob"
                and contact.get("lastName") == "Builder"
                and contact.get("email") == "bob@builder.io"
                and contact.get("phone") == "+1 (555) 123-4567"
                and contact.get("company") == "BuildCo"
                and contact.get("jobTitle") == "Foreman"):
            return True, "Contact Bob Builder with all specified fields exists."
    return False, ("No contact found with firstName 'Bob', lastName 'Builder', "
                   "email 'bob@builder.io', phone '+1 (555) 123-4567', "
                   "company 'BuildCo', jobTitle 'Foreman'.")
