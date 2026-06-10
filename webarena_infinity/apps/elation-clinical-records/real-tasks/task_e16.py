import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    for cat in categories:
        if cat.get("name") == "Care Plan Review":
            return False, "Category 'Care Plan Review' still exists."

    return True, "Successfully verified that 'Care Plan Review' category has been deleted."
