import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that a letter was sent to the older BPH patient (Frank DeLuca, pat_19) and the
    'Chronic Care' tag was added to the younger one (Philip Tran, pat_43)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}
    errors = []

    # 1. Check for new letter sent to pat_19 (Frank DeLuca, the older patient)
    letter_found = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("id") not in seed_letter_ids
                and ltr.get("patientId") == "pat_19"
                and ltr.get("direction") == "to_patient"
                and not ltr.get("isDraft", False)):
            letter_found = True
            break

    if not letter_found:
        errors.append("No new sent letter found for pat_19 (Frank DeLuca, older BPH patient)")

    # 2. Check 'Chronic Care' tag on pat_43 (Philip Tran, the younger patient)
    pat_43 = None
    for p in state.get("patients", []):
        if p.get("id") == "pat_43":
            pat_43 = p
            break

    if not pat_43:
        errors.append("Patient pat_43 (Philip Tran) not found")
    elif "Chronic Care" not in pat_43.get("tags", []):
        errors.append(f"'Chronic Care' not in pat_43 tags. Current tags: {pat_43.get('tags', [])}")

    if errors:
        return False, "; ".join(errors)

    return True, "Letter sent to pat_19 (older BPH patient) and 'Chronic Care' tag added to pat_43 (younger)"
