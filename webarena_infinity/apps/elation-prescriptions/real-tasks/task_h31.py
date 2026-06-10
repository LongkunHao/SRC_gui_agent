import requests


def verify(server_url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return False, f"Failed to fetch state: HTTP {resp.status_code}"
        state = resp.json()
    except Exception as e:
        return False, f"Error fetching state: {e}"

    templates = state.get("rxTemplates", [])
    tpl_names = [t.get("medicationName", "") for t in templates]

    # Check Amlodipine 10mg template exists
    amlodipine_10 = None
    for tpl in templates:
        name = tpl.get("medicationName", "").lower()
        if "amlodipine" in name and "10mg" in name:
            amlodipine_10 = tpl
            break
    if amlodipine_10 is None:
        return False, "No Amlodipine 10mg Rx template found"

    if amlodipine_10.get("qty") != 30:
        return False, f"Amlodipine 10mg template qty is {amlodipine_10.get('qty')}, expected 30"
    if amlodipine_10.get("refills") != 3:
        return False, f"Amlodipine 10mg template refills is {amlodipine_10.get('refills')}, expected 3"
    if amlodipine_10.get("daysSupply") != 30:
        return False, f"Amlodipine 10mg template daysSupply is {amlodipine_10.get('daysSupply')}, expected 30"

    # Check Amlodipine 5mg template was deleted
    for tpl in templates:
        name = tpl.get("medicationName", "")
        if name == "Amlodipine 5mg tablet":
            return False, "Amlodipine 5mg tablet template still exists, should be deleted"

    return True, "Amlodipine 10mg template created and Amlodipine 5mg template deleted"
