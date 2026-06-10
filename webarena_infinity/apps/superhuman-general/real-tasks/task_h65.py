import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Executive dinner email (id 12, from Patrick) lists:
    # Nate (CTO) = nate.patel@acmecorp.com
    # Tom (VP Engineering) = tom.bradley@acmecorp.com

    # Find a reply to Kevin Zhao's quantum computing email
    found = None
    for e in state.get("emails", []):
        if (e["from"]["email"] == "alex.morgan@acmecorp.com"
                and not e.get("isDraft")):
            to_emails = {r["email"] for r in e.get("to", [])}
            if "kevin.zhao@quantumlab.tech" in to_emails:
                subj = e.get("subject", "").lower()
                if "quantum" in subj:
                    found = e
                    break

    if not found:
        return False, "No reply to Kevin Zhao's quantum computing email found."

    cc_emails = {r["email"] for r in found.get("cc", [])}
    required_cc = {"nate.patel@acmecorp.com", "tom.bradley@acmecorp.com"}
    missing = required_cc - cc_emails
    if missing:
        return False, f"Missing CC: {', '.join(missing)}. CC has: {', '.join(cc_emails)}"

    return True, "Reply to Kevin Zhao sent with CTO and VP Engineering on CC."
