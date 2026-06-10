import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Reminder emails from people outside Acme Corp (non @acmecorp.com senders):
    # - id 64: James O'Brien (legalwise.com) - "Patent Filing Deadline - April 15"
    # - id 65: David Kim (financeplus.com) - "Re: Payment Terms Discussion"
    # - id 66: Aisha Mohammed (edtech.academy) - "EdTech Academy Partnership"
    # - id 67: Yuki Tanaka (tokyotech.jp) - "TokyoTech Conference Invitation"
    external_reminders = [
        ("Patent Filing Deadline - April 15", "james.obrien@legalwise.com"),
        ("Re: Payment Terms Discussion", "david.kim@financeplus.com"),
        ("EdTech Academy Partnership", "aisha.m@edtech.academy"),
        ("TokyoTech Conference Invitation", "yuki.t@tokyotech.jp"),
    ]

    not_archived = []
    for subj, sender in external_reminders:
        for e in state.get("emails", []):
            if e["subject"] == subj and e["from"]["email"] == sender:
                if not e.get("isDone", False):
                    not_archived.append(f"'{subj}' from {sender}")
                break
        else:
            return False, f"Email '{subj}' from {sender} not found."

    if not_archived:
        return False, f"{len(not_archived)} external reminder(s) not archived: {'; '.join(not_archived)}"

    return True, "All 4 reminder emails from external contacts have been archived."
