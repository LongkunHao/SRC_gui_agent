import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Marcus Johnson by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Johnson":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Johnson' not found."

    patient_id = patient.get("id")

    # Find problem 'Essential Hypertension, Uncontrolled' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Essential Hypertension, Uncontrolled"):
            dx_date = problem.get("dxDate", "")
            if dx_date == "2015-01-10":
                return True, ("Problem 'Essential Hypertension, Uncontrolled' for Marcus Johnson "
                              "has dxDate '2015-01-10'.")
            else:
                return False, (f"Problem 'Essential Hypertension, Uncontrolled' for Marcus Johnson "
                               f"has incorrect dxDate. Expected: '2015-01-10', Got: '{dx_date}'")

    return False, "Problem 'Essential Hypertension, Uncontrolled' not found for Marcus Johnson."
