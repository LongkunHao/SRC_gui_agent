import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify CPT code '99201' removed."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    cpt_codes = state.get("practiceSettings", {}).get("cptCodes", [])

    for c in cpt_codes:
        if c.get("code") == "99201":
            return False, "CPT code '99201' still exists in cptCodes, expected it to be removed"

    return True, "CPT code '99201' correctly removed from cptCodes"
