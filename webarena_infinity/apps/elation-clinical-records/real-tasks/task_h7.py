import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Rodriguez-Martinez (pat_004)
    patients = state.get("patients", [])
    rodriguez = None
    for p in patients:
        if p.get("lastName") == "Rodriguez-Martinez":
            rodriguez = p
            break
    if not rodriguez:
        return False, "Patient with lastName 'Rodriguez-Martinez' not found."

    tags = rodriguez.get("tags", [])

    if tags == ["Inhaler-Review"]:
        return True, "Rodriguez-Martinez's tags are exactly ['Inhaler-Review'] as expected."

    if "Inhaler-Review" not in tags:
        return False, f"Rodriguez-Martinez's tags do not include 'Inhaler-Review'. Current tags: {tags}"

    if len(tags) != 1:
        return False, (
            f"Rodriguez-Martinez should have only ['Inhaler-Review'] but has: {tags}. "
            f"Old tags should have been removed."
        )

    return False, f"Rodriguez-Martinez's tags are {tags}, expected exactly ['Inhaler-Review']."
