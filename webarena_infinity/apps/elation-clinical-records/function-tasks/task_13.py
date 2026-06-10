import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Priya Sharma by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Sharma":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Sharma' not found."

    patient_id = patient.get("id")

    # Find problem with title 'Urinary Tract Infection' and icd10='N39.0' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Urinary Tract Infection" and
                problem.get("icd10") == "N39.0"):
            return True, "Problem 'Urinary Tract Infection' with ICD-10 'N39.0' found for Priya Sharma."

    return False, "Problem 'Urinary Tract Infection' with ICD-10 'N39.0' not found for Priya Sharma."
