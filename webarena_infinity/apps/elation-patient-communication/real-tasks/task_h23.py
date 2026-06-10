import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify nurse practitioner has virtual visits activated with correct instructions."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Jessica Okafor (prov_3) is the nurse practitioner
    np_prov = None
    for prov in state.get("providers", []):
        if prov.get("role") == "nurse_practitioner":
            np_prov = prov
            break

    if np_prov is None:
        return False, "No nurse practitioner found in providers"

    if not np_prov.get("virtualVisitActivated"):
        return False, (
            f"Nurse practitioner {np_prov.get('firstName')} {np_prov.get('lastName')} "
            f"still has virtual visits deactivated"
        )

    instructions = np_prov.get("virtualVisitInstructions", "")
    if "zoom.us/j/5551234567" not in instructions:
        return False, (
            f"Virtual visit instructions don't contain expected Zoom link. "
            f"Got: {instructions!r}"
        )

    return True, (
        f"Nurse practitioner {np_prov.get('firstName')} {np_prov.get('lastName')} "
        f"has virtual visits activated with correct instructions"
    )
