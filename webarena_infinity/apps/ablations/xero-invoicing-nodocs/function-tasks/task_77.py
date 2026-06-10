import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    con = next((c for c in state["contacts"] if c["name"] == "Tasman Bay Charters"), None)
    if not con:
        return False, "Contact 'Tasman Bay Charters' not found."
    if con["email"] != "info@tasmanbay.co.nz":
        return False, f"Expected email 'info@tasmanbay.co.nz', got '{con['email']}'"
    return True, "Contact 'Tasman Bay Charters' created correctly."
