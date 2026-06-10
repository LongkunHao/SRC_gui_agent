import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Vanguard Security repeating invoice (rep_004)
    ri = next(
        (r for r in state.get("repeatingInvoices", []) if r.get("id") == "rep_004"),
        None
    )
    if ri is None:
        return False, "Vanguard Security repeating invoice (rep_004) not found."

    if ri.get("frequency") != "fortnightly":
        return False, f"Expected frequency 'fortnightly', got '{ri.get('frequency')}'."

    end_date = ri.get("endDate", "")
    if not end_date.startswith("2026-06"):
        return False, f"Expected end date in June 2026, got '{end_date}'."

    return True, "Vanguard Security repeating invoice: frequency=fortnightly, endDate=June 2026."
