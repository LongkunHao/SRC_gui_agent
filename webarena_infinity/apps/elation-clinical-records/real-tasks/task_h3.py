import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Zhao (pat_010)
    patients = state.get("patients", [])
    zhao = None
    for p in patients:
        if p.get("lastName") == "Zhao":
            zhao = p
            break
    if not zhao:
        return False, "Patient with lastName 'Zhao' not found."

    patient_id = zhao.get("id", "pat_010")

    problems = state.get("problems", [])
    zhao_problems = [pr for pr in problems if pr.get("patientId") == patient_id]

    # Check 1: Osteopenia with ICD-10 M85.80
    osteopenia_found = False
    for pr in zhao_problems:
        title = (pr.get("title") or "").lower()
        icd10 = (pr.get("icd10") or "").strip()
        if "osteopenia" in title and icd10 == "M85.80":
            osteopenia_found = True
            break

    if not osteopenia_found:
        return False, "No problem 'Osteopenia' with ICD-10 code 'M85.80' found for Zhao."

    # Check 2: Osteoporosis problem marked as Controlled
    osteoporosis_controlled = False
    for pr in zhao_problems:
        title = (pr.get("title") or "").lower()
        if "osteoporosis" in title:
            if pr.get("status") == "Controlled":
                osteoporosis_controlled = True
                break

    if not osteoporosis_controlled:
        # Find current status for diagnostics
        osteo_statuses = [
            f"{pr.get('title')}={pr.get('status')}"
            for pr in zhao_problems if "osteoporosis" in (pr.get("title") or "").lower()
        ]
        return False, (
            f"Zhao's osteoporosis problem is not marked as 'Controlled'. "
            f"Current osteoporosis problems: {osteo_statuses if osteo_statuses else 'none found'}"
        )

    return True, "Zhao has 'Osteopenia' (M85.80) added and osteoporosis marked as Controlled."
