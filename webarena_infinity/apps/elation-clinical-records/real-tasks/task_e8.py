import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    target = None
    for cat in categories:
        if cat.get("name") == "Procedure":
            target = cat
            break

    if target is None:
        return False, "Could not find category with name='Procedure'."

    count_mips = target.get("countForMIPS")
    if count_mips is not False:
        return False, f"Category 'Procedure' countForMIPS is {count_mips}, expected False."

    return True, "Successfully verified that MIPS is disabled for the 'Procedure' category."
