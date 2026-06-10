import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the email "Global Health Initiative - Sponsorship Request" from "Ana Gutierrez"
    target_email = None
    for e in state.get("emails", []):
        if (e.get("subject") == "Global Health Initiative - Sponsorship Request"
                and e.get("from", {}).get("name") == "Ana Gutierrez"):
            target_email = e
            break

    if not target_email:
        return False, "Could not find email 'Global Health Initiative - Sponsorship Request' from Ana Gutierrez."

    # Check that isTrashed is True
    if target_email.get("isTrashed") == True:
        return True, "Ana Gutierrez's sponsorship email has been successfully moved to trash."
    else:
        return False, f"Email is not trashed. isTrashed: {target_email.get('isTrashed')}"
