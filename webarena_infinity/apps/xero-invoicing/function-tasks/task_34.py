import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    ri = next((r for r in state["repeatingInvoices"] if r["id"] == "rep_005"), None)
    if ri is not None:
        return False, "Repeating invoice rep_005 (Summit Health Group) still exists."

    return True, "Draft repeating invoice for Summit Health Group deleted."
