import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state["emails"]:
        if e["subject"] == "Logistics Update - Office Equipment Delivery" and e["from"]["name"] == "Carlos Mendez":
            if e["isDone"] is True:
                return True, "The logistics email from Carlos Mendez is archived."
            return False, f"The logistics email from Carlos Mendez is not archived (isDone={e['isDone']})."

    return False, "Could not find the logistics email from Carlos Mendez."
