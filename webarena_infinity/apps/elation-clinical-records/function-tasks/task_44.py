import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    has_workers_compensation = False
    has_workers_comp = False

    for cat in categories:
        if cat.get("name") == "Workers Compensation":
            has_workers_compensation = True
        if cat.get("name") == "Workers Comp":
            has_workers_comp = True

    if not has_workers_compensation:
        return False, "No category with name 'Workers Compensation' found in visitNoteCategories."
    if has_workers_comp:
        return False, "Category with name 'Workers Comp' still exists in visitNoteCategories; it should have been renamed or removed."

    return True, "Found 'Workers Compensation' category and no 'Workers Comp' category exists."
