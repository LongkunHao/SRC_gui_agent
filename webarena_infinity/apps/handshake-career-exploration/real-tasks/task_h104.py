"""
Task: Find the employer whose affiliated companies include 'Tableau'.
RSVP to their upcoming cloud careers event and follow them.

Discovery: Tableau → Salesforce (emp_19). Event: evt_10 (Futureforce).

Verify:
(1) evt_10 RSVP'd
(2) emp_19 in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    events = state.get("events", [])
    evt_10 = next((e for e in events if e.get("id") == "evt_10"), None)
    if evt_10 is None:
        errors.append("evt_10 not found.")
    elif not evt_10.get("rsvped"):
        errors.append(f"evt_10 not RSVP'd. rsvped={evt_10.get('rsvped')}")

    followed = state.get("currentUser", {}).get("followedEmployerIds", [])
    if "emp_19" not in followed:
        errors.append(f"emp_19 (Salesforce) not followed. Current: {followed}")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Salesforce identified via Tableau affiliation. "
        "Futureforce event RSVP'd and Salesforce followed."
    )
