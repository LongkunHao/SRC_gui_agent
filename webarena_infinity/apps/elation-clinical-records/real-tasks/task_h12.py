import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Sharma (pat_006)
    patients = state.get("patients", [])
    sharma = None
    for p in patients:
        if p.get("lastName") == "Sharma":
            sharma = p
            break
    if not sharma:
        return False, "Patient with lastName 'Sharma' not found."

    patient_id = sharma.get("id", "pat_006")

    problems = state.get("problems", [])
    sharma_problems = [pr for pr in problems if pr.get("patientId") == patient_id]

    # Check 1: Urinary Tract Infection with N39.0, Active
    uti_found = False
    for pr in sharma_problems:
        title = (pr.get("title") or "").lower()
        icd10 = (pr.get("icd10") or "").strip()
        status = pr.get("status", "")
        if "urinary tract infection" in title and icd10 == "N39.0" and status == "Active":
            uti_found = True
            break

    # Check 2: Iron Deficiency Anemia with D50.9, Active
    anemia_found = False
    for pr in sharma_problems:
        title = (pr.get("title") or "").lower()
        icd10 = (pr.get("icd10") or "").strip()
        status = pr.get("status", "")
        if "iron deficiency anemia" in title and icd10 == "D50.9" and status == "Active":
            anemia_found = True
            break

    errors = []
    if not uti_found:
        return False, "No active 'Urinary Tract Infection' with ICD-10 'N39.0' found for Sharma."
    if not anemia_found:
        return False, "No active 'Iron Deficiency Anemia' with ICD-10 'D50.9' found for Sharma."

    return True, "Both problems added to Sharma: 'Urinary Tract Infection' (N39.0) and 'Iron Deficiency Anemia' (D50.9), both Active."
