import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    for cat in categories:
        if cat.get("name") == "Procedure":
            if cat.get("countForMIPS") is False:
                return True, "Found 'Procedure' category with countForMIPS==False."
            else:
                return False, f"Found 'Procedure' category but countForMIPS is {cat.get('countForMIPS')}, expected False."

    return False, "No category with name 'Procedure' found in visitNoteCategories."
