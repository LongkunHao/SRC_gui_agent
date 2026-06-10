import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # CN-0009 (Coastal Living Interiors, awaiting_payment) -> should be voided
    cn_009 = next((cn for cn in state.get("creditNotes", []) if cn.get("number") == "CN-0009"), None)
    if cn_009 is None:
        return False, "CN-0009 not found."
    if cn_009.get("status") != "voided":
        return False, f"Expected CN-0009 status 'voided', got '{cn_009.get('status')}'."

    # CN-0011 (Pacific Freight Lines, draft) -> should be deleted
    cn_011 = next((cn for cn in state.get("creditNotes", []) if cn.get("number") == "CN-0011"), None)
    if cn_011 is None:
        # Deleted could mean removed entirely
        return True, "CN-0009 voided, CN-0011 deleted (removed)."
    if cn_011.get("status") != "deleted":
        return False, f"Expected CN-0011 status 'deleted', got '{cn_011.get('status')}'."

    return True, "CN-0009 (Coastal Living) voided, CN-0011 (Pacific Freight) deleted."
