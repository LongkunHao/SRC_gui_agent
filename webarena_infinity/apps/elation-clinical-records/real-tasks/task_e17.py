import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Bergstrom":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Bergstrom'."

    patient_id = patient.get("id")
    problems = state.get("problems", [])
    target_problem = None
    for prob in problems:
        if prob.get("patientId") == patient_id:
            title = prob.get("title", "")
            if "Major Depressive Disorder" in title or "Depression" in title:
                target_problem = prob
                break

    if target_problem is None:
        return False, f"Could not find a depression-related problem for patient Bergstrom (patientId={patient_id})."

    status = target_problem.get("status", "")
    if status != "Active":
        return False, f"Problem '{target_problem.get('title')}' status is '{status}', expected 'Active'."

    return True, f"Successfully verified that Thomas Bergstrom's '{target_problem.get('title')}' is marked as Active."
