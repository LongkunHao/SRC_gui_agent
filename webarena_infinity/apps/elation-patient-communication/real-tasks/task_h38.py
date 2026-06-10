import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify all uninvited patients now invited and Dr. Chen's sharing default is 4."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Previously uninvited patients: pat_9, pat_15, pat_23, pat_31, pat_37, pat_42
    uninvited_ids = {"pat_9", "pat_15", "pat_23", "pat_31", "pat_37", "pat_42"}

    still_uninvited = []
    for pat in state.get("patients", []):
        if pat.get("id") in uninvited_ids:
            if pat.get("passportStatus") != "invited":
                name = f"{pat.get('firstName', '')} {pat.get('lastName', '')}"
                still_uninvited.append(
                    f"{name} (status: {pat.get('passportStatus')})"
                )

    if still_uninvited:
        return False, (
            f"Patients still uninvited: {', '.join(still_uninvited)}"
        )

    # Check Dr. Chen's sharing default
    for prov in state.get("providers", []):
        if prov.get("id") == "prov_1":
            if prov.get("sharingDefault") != 4:
                return False, (
                    f"Dr. Chen's sharing default is {prov.get('sharingDefault')}, "
                    f"expected 4"
                )
            break

    return True, "All 6 uninvited patients now invited and Dr. Chen's sharing default set to 4"
