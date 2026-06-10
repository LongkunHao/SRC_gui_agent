import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Robert Henderson by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Henderson":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Henderson' not found."

    patient_id = patient.get("id")
    expected_synopsis = "A1C 6.8% at last check. Well-controlled on current regimen."

    # Find problem 'Type 2 Diabetes Mellitus' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Type 2 Diabetes Mellitus"):
            synopsis = problem.get("synopsis", "")
            if synopsis == expected_synopsis:
                return True, "Problem 'Type 2 Diabetes Mellitus' for Robert Henderson has the correct synopsis."
            else:
                return False, (f"Problem 'Type 2 Diabetes Mellitus' for Robert Henderson has incorrect synopsis. "
                               f"Expected: '{expected_synopsis}', Got: '{synopsis}'")

    return False, "Problem 'Type 2 Diabetes Mellitus' not found for Robert Henderson."
