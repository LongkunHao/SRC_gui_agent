import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    linked_services = state.get("linkedServices", [])
    for service in linked_services:
        if service.get("name") == "Google Shopping":
            if service.get("isLinked") is True:
                return True, "Google Shopping is linked."
            else:
                return False, f"Google Shopping is not linked. isLinked={service.get('isLinked')}"
    return False, "Google Shopping service not found in linkedServices."
