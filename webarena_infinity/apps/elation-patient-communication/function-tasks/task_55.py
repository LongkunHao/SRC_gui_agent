import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify CPT code '99205' added with correct description."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    cpt_codes = state.get("practiceSettings", {}).get("cptCodes", [])

    code_entry = None
    for c in cpt_codes:
        if c.get("code") == "99205":
            code_entry = c
            break

    if code_entry is None:
        return False, "CPT code '99205' not found in practiceSettings.cptCodes"

    description = code_entry.get("description")
    if description != "Office visit, new patient, high complexity":
        return False, f"CPT code '99205' description is '{description}', expected 'Office visit, new patient, high complexity'"

    return True, "CPT code '99205' correctly added with description 'Office visit, new patient, high complexity'"
