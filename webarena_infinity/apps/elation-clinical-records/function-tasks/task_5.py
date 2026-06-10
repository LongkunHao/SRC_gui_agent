import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient James Fitzgerald by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Fitzgerald":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Fitzgerald' not found."

    patient_id = patient.get("id")

    # Find problem with title 'Acute Sinusitis' and icd10='J01.90' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Acute Sinusitis" and
                problem.get("icd10") == "J01.90"):
            return True, "Problem 'Acute Sinusitis' with ICD-10 'J01.90' found for James Fitzgerald."

    return False, "Problem 'Acute Sinusitis' with ICD-10 'J01.90' not found for James Fitzgerald."
