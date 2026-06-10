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
    tpl_names = [t.get("medicationName") for t in templates]

    # Three temporary meds:
    expected = [
        {
            "medicationName": "Amoxicillin 500mg capsule",
            "qty": 30, "unit": "capsules", "daysSupply": 10, "refills": 0,
        },
        {
            "medicationName": "Prednisone 10mg tablet",
            "qty": 21, "unit": "tablets", "daysSupply": 7, "refills": 0,
        },
        {
            "medicationName": "Ciprofloxacin 500mg tablet",
            "qty": 14, "unit": "tablets", "daysSupply": 7, "refills": 0,
        },
    ]

    for exp in expected:
        name = exp["medicationName"]
        tpl = None
        for t in templates:
            if t.get("medicationName") == name:
                tpl = t
                break
        if tpl is None:
            # Check if template exists with slightly different name
            found = any(name.lower() in t.get("medicationName", "").lower() for t in templates)
            if not found:
                return False, f"Template for '{name}' not found"
            else:
                continue

        if tpl.get("qty") != exp["qty"]:
            return False, f"Template '{name}' qty is {tpl.get('qty')}, expected {exp['qty']}"
        if tpl.get("daysSupply") != exp["daysSupply"]:
            return False, f"Template '{name}' daysSupply is {tpl.get('daysSupply')}, expected {exp['daysSupply']}"
        if tpl.get("refills") != 0:
            return False, f"Template '{name}' refills is {tpl.get('refills')}, expected 0"

    return True, "Rx templates created for all three temporary medications"
