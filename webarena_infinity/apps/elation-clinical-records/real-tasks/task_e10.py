import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    found_old = False
    found_new = False
    for cat in categories:
        if cat.get("name") == "Workers Comp":
            found_old = True
        if cat.get("name") == "Workers Compensation":
            found_new = True

    if found_old:
        return False, "Category 'Workers Comp' still exists (has not been renamed)."

    if not found_new:
        return False, "Category 'Workers Compensation' not found. The rename did not happen correctly."

    return True, "Successfully verified that 'Workers Comp' has been renamed to 'Workers Compensation'."
