import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # The repeating invoice that saves as drafts is rep_002 (CloudNine)
    rep = next(
        (r for r in state.get("repeatingInvoices", []) if r.get("id") == "rep_002"),
        None
    )
    if rep is None:
        return False, "Repeating invoice rep_002 not found."

    if rep.get("frequency") != "quarterly":
        return False, f"Expected frequency 'quarterly', got '{rep.get('frequency')}'."

    ref = rep.get("reference", "")
    if ref != "QUARTERLY-REVIEW":
        return False, f"Expected reference 'QUARTERLY-REVIEW', got '{ref}'."

    return True, "Repeating invoice rep_002 updated: quarterly frequency, reference 'QUARTERLY-REVIEW'."
