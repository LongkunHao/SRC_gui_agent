import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # rep_003 is Cascade Software repeating invoice
    ri = next((r for r in state.get("repeatingInvoices", []) if r.get("id") == "rep_003"), None)
    if ri is None:
        return False, "Cascade Software repeating invoice (rep_003) not found."

    errors = []

    if ri.get("frequency") != "fortnightly":
        errors.append(f"Expected frequency 'fortnightly', got '{ri.get('frequency')}'.")

    end_date = ri.get("endDate", "")
    if not end_date or "2026-09" not in end_date:
        errors.append(f"Expected end date in September 2026, got '{end_date}'.")

    if ri.get("saveAs") != "draft":
        errors.append(f"Expected saveAs 'draft', got '{ri.get('saveAs')}'.")

    if errors:
        return False, " ".join(errors)

    return True, "Cascade Software repeating invoice updated: fortnightly, end Sep 2026, saveAs draft."
