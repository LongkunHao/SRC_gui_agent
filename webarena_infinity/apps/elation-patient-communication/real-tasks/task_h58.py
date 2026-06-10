import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify separate letters sent to both Mental Health tagged patients
    (pat_12 Rachel Steinberg, pat_22 Christine Lee) with doNotAllowResponse=true."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Mental Health tagged patients
    target_ids = {"pat_12", "pat_22"}
    target_names = {
        "pat_12": "Rachel Steinberg",
        "pat_22": "Christine Lee"
    }

    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    # Track which target patients got a valid letter
    patients_with_letter = {}

    for ltr in state.get("patientLetters", []):
        ltr_id = ltr.get("id", "")
        if ltr_id in seed_letter_ids:
            continue

        patient_id = ltr.get("patientId", "")
        if patient_id not in target_ids:
            continue

        direction = ltr.get("direction", "")
        do_not_allow = ltr.get("doNotAllowResponse", False)
        is_draft = ltr.get("isDraft", True)

        if direction == "to_patient" and do_not_allow and not is_draft:
            patients_with_letter[patient_id] = ltr_id

    missing = target_ids - set(patients_with_letter.keys())
    if missing:
        missing_names = [f"{target_names[pid]} ({pid})" for pid in sorted(missing)]
        # Check if there are letters that partially match
        partial = {}
        for ltr in state.get("patientLetters", []):
            ltr_id = ltr.get("id", "")
            if ltr_id in seed_letter_ids:
                continue
            patient_id = ltr.get("patientId", "")
            if patient_id in missing:
                partial[patient_id] = (
                    f"direction={ltr.get('direction')}, "
                    f"doNotAllowResponse={ltr.get('doNotAllowResponse')}, "
                    f"isDraft={ltr.get('isDraft')}"
                )
        detail = ""
        if partial:
            detail = ". Found partial matches: " + "; ".join(
                f"{target_names[pid]}: {info}" for pid, info in partial.items()
            )
        return False, (
            f"Missing valid letters (to_patient, doNotAllowResponse=true, not draft) for: "
            f"{', '.join(missing_names)}{detail}"
        )

    return True, (
        "Letters sent to both Rachel Steinberg (pat_12) and Christine Lee (pat_22) "
        "with doNotAllowResponse=true"
    )
