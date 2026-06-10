import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Lunch with Marcus on March 7 (evt_3): Marcus Williams (marcus.w@designhub.io)
    # His inbox email: "New Brand Assets - Review Needed"

    travel_id = None
    for label in state.get("labels", []):
        if label["name"] == "Travel":
            travel_id = label["id"]
            break
    if not travel_id:
        return False, "Travel label not found."

    target = None
    for e in state.get("emails", []):
        if (e["subject"] == "New Brand Assets - Review Needed"
                and e["from"]["email"] == "marcus.w@designhub.io"):
            target = e
            break

    if not target:
        return False, "Marcus Williams' brand assets email not found."

    if travel_id not in target.get("labels", []):
        return False, "Marcus's email does not have the 'Travel' label."

    remind = target.get("remindAt")
    if not remind:
        return False, "No reminder set on Marcus's email."

    if not remind.startswith("2026-03-11"):
        return False, f"Reminder is set to '{remind}', expected March 11."

    return True, "'Travel' label and March 11 reminder set on Marcus's email."
