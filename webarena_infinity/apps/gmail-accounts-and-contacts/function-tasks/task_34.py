import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    linked_services = state.get("linkedServices", [])
    svc_1 = None
    for svc in linked_services:
        if svc.get("id") == "svc_1":
            svc_1 = svc
            break

    if svc_1 is None:
        return False, "Linked service 'svc_1' (Google Search) not found."

    if svc_1.get("name") != "Google Search":
        return False, f"Service 'svc_1' name is '{svc_1.get('name')}', expected 'Google Search'."

    if svc_1.get("isLinked") is not False:
        return False, f"Service 'Google Search' (svc_1) has isLinked={svc_1.get('isLinked')}, expected False."

    return True, "Linked service 'Google Search' (svc_1) has isLinked=False."
