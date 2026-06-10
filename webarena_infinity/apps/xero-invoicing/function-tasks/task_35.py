import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ri = next((r for r in state["repeatingInvoices"] if r["id"] == "rep_001"), None)
    if not ri:
        return False, "Repeating invoice rep_001 not found."

    if ri["endDate"] != "2027-06-30":
        return False, f"Repeating invoice endDate is '{ri['endDate']}', expected '2027-06-30'."

    return True, "Repeating invoice for Greenfield Organics end date set to 2027-06-30."
