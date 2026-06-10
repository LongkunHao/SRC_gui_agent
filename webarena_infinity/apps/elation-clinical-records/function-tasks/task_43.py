import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    for cat in categories:
        if cat.get("name") == "Behavioral Health":
            if cat.get("countForMIPS") is True:
                return True, "Found 'Behavioral Health' category with countForMIPS==True."
            else:
                return False, f"Found 'Behavioral Health' category but countForMIPS is {cat.get('countForMIPS')}, expected True."

    return False, "No category with name 'Behavioral Health' found in visitNoteCategories."
