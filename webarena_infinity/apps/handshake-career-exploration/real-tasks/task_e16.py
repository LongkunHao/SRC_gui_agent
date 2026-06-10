import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find event evt_10 (Salesforce Futureforce cloud careers session)
    events = state.get("events", [])
    evt_10 = None
    for event in events:
        if event.get("id") == "evt_10":
            evt_10 = event
            break

    if evt_10 is None:
        return False, "Event evt_10 (Salesforce Futureforce) not found in state."

    if not evt_10.get("rsvped"):
        return False, f"Event evt_10 rsvped is {evt_10.get('rsvped')}, expected True."

    rsvp_count = evt_10.get("rsvpCount", 0)
    if rsvp_count <= 123:
        return False, f"Event evt_10 rsvpCount is {rsvp_count}, expected > 123."

    return True, f"Successfully signed up for Salesforce Futureforce session. rsvped=True, rsvpCount={rsvp_count} > 123."
