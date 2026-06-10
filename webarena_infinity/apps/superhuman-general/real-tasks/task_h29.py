import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    snippets = state.get("snippets", [])

    # Snippets with response rate below 30% in seed:
    # - "Out of Office" (11%)
    # - "[Engineering] Bug Report Response" (28%)
    # - "Decline Politely" (20%)
    should_be_deleted = {"Out of Office", "[Engineering] Bug Report Response", "Decline Politely"}
    still_present = []
    for s in snippets:
        if s["name"] in should_be_deleted:
            still_present.append(f"'{s['name']}' (response rate: {s.get('metrics', {}).get('responseRate', '?')})")

    if still_present:
        return False, f"Snippets that should have been deleted (response rate < 30%) still exist: {', '.join(still_present)}"

    # Verify snippets with >= 30% response rate still exist
    should_remain = {"Meeting Follow-up", "Introduction", "Scheduling Request",
                     "[Sales] Product Demo", "[Sales] Proposal Follow-up",
                     "[HR] Interview Confirmation", "Thank You", "Quick Check-in",
                     "[Marketing] Event Invitation"}
    remaining_names = {s["name"] for s in snippets}
    missing = should_remain - remaining_names
    if missing:
        return False, f"Snippets that should NOT have been deleted are missing: {', '.join(missing)}"

    return True, "All 3 snippets with response rate below 30% have been deleted."
