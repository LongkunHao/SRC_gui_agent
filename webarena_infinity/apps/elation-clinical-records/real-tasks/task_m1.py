import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Fitzgerald":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Fitzgerald'."

    patient_id = patient.get("id")
    problems = state.get("problems", [])
    target_problem = None
    for prob in problems:
        if prob.get("patientId") == patient_id and prob.get("title") == "Acute Sinusitis":
            target_problem = prob
            break

    if target_problem is None:
        patient_problems = [prob.get("title") for prob in problems if prob.get("patientId") == patient_id]
        return False, f"Could not find problem 'Acute Sinusitis' for patient Fitzgerald (patientId={patient_id}). Current problems: {patient_problems}"

    icd10 = target_problem.get("icd10", "")
    if icd10 != "J01.90":
        return False, f"Problem 'Acute Sinusitis' has ICD-10 code '{icd10}', expected 'J01.90'."

    return True, "Successfully verified that 'Acute Sinusitis' (J01.90) was added to James Fitzgerald's problem list."
