import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    linked_services = state.get("linkedServices", [])
    for service in linked_services:
        if service.get("name") == "YouTube":
            if service.get("isLinked") is False:
                return True, "YouTube is not linked as expected."
            else:
                return False, f"YouTube is still linked. isLinked={service.get('isLinked')}"
    return False, "YouTube service not found in linkedServices."
