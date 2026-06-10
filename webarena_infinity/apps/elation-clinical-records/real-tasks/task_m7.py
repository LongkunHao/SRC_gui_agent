import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    categories = state.get("visitNoteCategories", [])
    target_cat = None
    for cat in categories:
        if cat.get("name") == "Behavioral Health":
            target_cat = cat
            break

    if target_cat is None:
        cat_names = [c.get("name") for c in categories]
        return False, f"Could not find category named 'Behavioral Health'. Current categories: {cat_names}"

    count_for_mips = target_cat.get("countForMIPS")
    if count_for_mips is not True:
        return False, f"Category 'Behavioral Health' countForMIPS is {count_for_mips}, expected True."

    return True, "Successfully verified that category 'Behavioral Health' was added with MIPS tracking enabled."
