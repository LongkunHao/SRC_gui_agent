import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rr_003 = next((rr for rr in state.get("refillRequests", []) if rr["id"] == "rr_003"), None)
    if rr_003 is None:
        return False, "Refill request rr_003 not found."

    if rr_003.get("status") != "modified":
        return False, f"Expected rr_003 status 'modified', got '{rr_003.get('status')}'."

    modified_details = rr_003.get("modifiedDetails", "")
    if "20mg" not in modified_details.lower():
        return False, f"Expected rr_003 modifiedDetails to contain '20mg', got '{modified_details}'."

    return True, "Margaret's Pantoprazole refill (rr_003) modified and approved with dose reduced to 20mg."
