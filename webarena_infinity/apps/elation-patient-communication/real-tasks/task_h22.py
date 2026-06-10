import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify all Diabetes Management patients have sharing level >= 3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Diabetes Management patients: pat_1, pat_11, pat_30, pat_35
    diabetes_mgmt_ids = {"pat_1", "pat_11", "pat_30", "pat_35"}

    below_3 = []
    for pat in state.get("patients", []):
        if pat.get("id") in diabetes_mgmt_ids:
            level = pat.get("passportSharingLevel", 0)
            if level < 3:
                name = f"{pat.get('firstName', '')} {pat.get('lastName', '')}"
                below_3.append(f"{name} (level {level})")

    if below_3:
        return False, (
            f"Diabetes Management patients still below sharing level 3: "
            f"{', '.join(below_3)}"
        )

    return True, "All Diabetes Management patients have sharing level >= 3"
