import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that all Geriatric-tagged patients with passport sharing level below 3 have been
    updated to level 3, and those already at 3 or above remain unchanged."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    patients = state.get("patients", [])
    if not patients:
        return False, "No patients found in state"

    # Build lookup
    patient_map = {p.get("id"): p for p in patients}

    # Patients that should have been updated to level 3 (were below 3)
    should_be_3 = ["pat_19", "pat_33", "pat_43", "pat_47"]
    # Patients that should remain at their existing level (already >= 3)
    should_stay = {
        "pat_3": 3, "pat_10": 3, "pat_24": 3, "pat_27": 3, "pat_36": 3, "pat_50": 3
    }

    errors = []

    for pid in should_be_3:
        p = patient_map.get(pid)
        if not p:
            errors.append(f"{pid} not found in state")
            continue
        level = p.get("passportSharingLevel")
        if level != 3:
            errors.append(f"{pid} sharing level is {level}, expected 3")

    for pid, expected in should_stay.items():
        p = patient_map.get(pid)
        if not p:
            errors.append(f"{pid} not found in state")
            continue
        level = p.get("passportSharingLevel")
        if level != expected:
            errors.append(f"{pid} sharing level changed to {level}, expected to remain {expected}")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All Geriatric patients below level 3 updated to 3 (pat_19, pat_33, pat_43, pat_47); "
        "patients already at 3+ remain unchanged"
    )
