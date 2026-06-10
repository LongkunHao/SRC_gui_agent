import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    target = None
    for cat in categories:
        if cat.get("name") == "Vaccination Only":
            target = cat
            break

    if target is None:
        return False, "Could not find category with name='Vaccination Only'."

    count_mips = target.get("countForMIPS")
    if count_mips is not True:
        return False, f"Category 'Vaccination Only' countForMIPS is {count_mips}, expected True."

    return True, "Successfully verified that MIPS is enabled for the 'Vaccination Only' category."
