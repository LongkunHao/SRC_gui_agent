import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify bulk letter sent to all New Patient tagged patients, no responses allowed."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # New Patient patients: pat_2, pat_5, pat_9, pat_31, pat_42
    new_patient_ids = {"pat_2", "pat_5", "pat_9", "pat_31", "pat_42"}

    seed_bulk_ids = {"bulk_1", "bulk_2", "bulk_3"}

    # Find new bulk letter
    new_bulk = None
    for bl in state.get("bulkLetters", []):
        if bl.get("id") not in seed_bulk_ids:
            new_bulk = bl
            break

    if new_bulk is None:
        return False, "No new bulk letter found in state"

    if new_bulk.get("allowResponse"):
        return False, (
            f"Bulk letter has allowResponse={new_bulk.get('allowResponse')}, expected False"
        )

    target_count = new_bulk.get("targetCount", 0)
    if target_count < 5:
        return False, (
            f"Bulk letter targetCount is {target_count}, expected at least 5 "
            f"(number of New Patient tagged patients)"
        )

    # Check individual letters were sent
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}
    patients_with_letter = set()
    for ltr in state.get("patientLetters", []):
        if (ltr.get("id") not in seed_letter_ids
                and ltr.get("direction") == "to_patient"
                and not ltr.get("isDraft", False)
                and ltr.get("patientId") in new_patient_ids):
            patients_with_letter.add(ltr.get("patientId"))

    missing = new_patient_ids - patients_with_letter
    if missing:
        return False, (
            f"Individual letters missing for New Patient patients: "
            f"{', '.join(sorted(missing))}"
        )

    return True, "Bulk letter sent to all 5 New Patient patients with responses disallowed"
