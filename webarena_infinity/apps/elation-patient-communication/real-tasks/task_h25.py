import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify letters sent to both VIP+Geriatric patients about wellness visits."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # VIP + Geriatric patients: pat_10 (Helen Matsumoto), pat_50 (Deborah Takahashi)
    target_ids = {"pat_10", "pat_50"}

    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    patients_with_letter = set()
    for ltr in state.get("patientLetters", []):
        if (ltr.get("id") not in seed_letter_ids
                and ltr.get("direction") == "to_patient"
                and not ltr.get("isDraft", False)
                and ltr.get("patientId") in target_ids):
            patients_with_letter.add(ltr.get("patientId"))

    missing = target_ids - patients_with_letter
    if missing:
        missing_names = []
        for pat in state.get("patients", []):
            if pat.get("id") in missing:
                missing_names.append(f"{pat.get('firstName')} {pat.get('lastName')}")
        return False, (
            f"Letters missing for VIP+Geriatric patients: {', '.join(missing_names)}"
        )

    return True, "Letters sent to both Helen Matsumoto and Deborah Takahashi about wellness visits"
