import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    for cat in categories:
        if cat.get("name") == "Vaccination Only":
            if cat.get("countForMIPS") is True:
                return True, "Found 'Vaccination Only' category with countForMIPS==True."
            else:
                return False, f"Found 'Vaccination Only' category but countForMIPS is {cat.get('countForMIPS')}, expected True."

    return False, "No category with name 'Vaccination Only' found in visitNoteCategories."
