import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Sofia Rodriguez-Martinez by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Rodriguez-Martinez":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Rodriguez-Martinez' not found."

    patient_id = patient.get("id")

    # Find problem with title 'Insomnia', icd10='G47.00', status='Controlled' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Insomnia" and
                problem.get("icd10") == "G47.00" and
                problem.get("status") == "Controlled"):
            return True, ("Problem 'Insomnia' with ICD-10 'G47.00' and status 'Controlled' "
                          "found for Sofia Rodriguez-Martinez.")

    # Provide more detail on what was found
    matching_title = []
    for problem in state.get("problems", []):
        if problem.get("patientId") == patient_id and problem.get("title") == "Insomnia":
            matching_title.append(f"icd10='{problem.get('icd10')}', status='{problem.get('status')}'")

    if matching_title:
        return False, (f"Problem 'Insomnia' found for Sofia Rodriguez-Martinez but with wrong attributes: "
                       f"{matching_title}. Expected icd10='G47.00' and status='Controlled'.")

    return False, "Problem 'Insomnia' with ICD-10 'G47.00' and status 'Controlled' not found for Sofia Rodriguez-Martinez."
