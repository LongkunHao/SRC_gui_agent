import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Priya's travel expenses email
    target = None
    for e in state.get("emails", []):
        if (e["subject"] == "Travel Expenses Approved"
                and e["from"]["email"] == "priya.sharma@acmecorp.com"):
            target = e
            break

    if not target:
        return False, "Priya Sharma's travel expenses email not found."

    # Should be moved from Done to inbox
    if target.get("isDone"):
        return False, "Travel expenses email is still in Done."

    # Should have Finance label
    finance_id = None
    for label in state.get("labels", []):
        if label["name"] == "Finance":
            finance_id = label["id"]
            break
    if not finance_id:
        return False, "Finance label not found."

    if finance_id not in target.get("labels", []):
        return False, "Travel expenses email missing 'Finance' label."

    # Should have reminder set for March 12
    remind = target.get("remindAt")
    if not remind:
        return False, "No reminder set on travel expenses email."

    if not remind.startswith("2026-03-12"):
        return False, f"Reminder set to '{remind}', expected March 12."

    return True, "Travel expenses email moved to inbox with Finance label and March 12 reminder."
