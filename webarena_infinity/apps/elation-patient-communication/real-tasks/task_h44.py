import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that a new letter has been sent to Robert Washington (pat_3) about his Warfarin check,
    with direction=to_patient, doNotAllowResponse=true, and isDraft=false."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    for ltr in state.get("patientLetters", []):
        if ltr.get("id") in seed_letter_ids:
            continue
        if (ltr.get("patientId") == "pat_3"
                and ltr.get("direction") == "to_patient"
                and ltr.get("doNotAllowResponse") is True
                and not ltr.get("isDraft", False)):
            return True, "New no-reply letter sent to pat_3 (Robert Washington) about Warfarin check"

    return False, "No new letter found for pat_3 with direction=to_patient, doNotAllowResponse=true, isDraft=false"
