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

    # Find problem 'Seasonal Allergic Rhinitis' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Seasonal Allergic Rhinitis"):
            status = problem.get("status", "")
            if status == "Active":
                return True, "Problem 'Seasonal Allergic Rhinitis' for Robert Henderson has status 'Active'."
            else:
                return False, (f"Problem 'Seasonal Allergic Rhinitis' for Robert Henderson has incorrect status. "
                               f"Expected: 'Active', Got: '{status}'")

    return False, "Problem 'Seasonal Allergic Rhinitis' not found for Robert Henderson."
