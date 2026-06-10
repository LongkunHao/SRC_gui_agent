import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    targets = [
        ("Q2 Product Roadmap - Final Review", "Sarah Chen"),
        ("Re: Series B Term Sheet Discussion", "Emily Rodriguez"),
        ("Budget Approval Needed - Marketing Campaign", "Priya Sharma"),
    ]

    errors = []
    for subject, from_name in targets:
        email = None
        for e in state.get("emails", []):
            if e["subject"] == subject and e["from"]["name"] == from_name:
                email = e
                break
        if not email:
            errors.append(f"Could not find '{subject}' from {from_name}.")
            continue
        if not email.get("isStarred", False):
            errors.append(f"'{subject}' is not starred.")
        if not email.get("isDone", False):
            errors.append(f"'{subject}' is not archived (isDone is not true).")

    if errors:
        return False, " | ".join(errors)

    return True, "All three emails (Sarah, Emily, Priya) are starred and archived."
