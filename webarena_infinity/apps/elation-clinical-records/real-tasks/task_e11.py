import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Johnson'."

    patient_id = patient.get("id")
    problems = state.get("problems", [])
    target_problem = None
    for prob in problems:
        if prob.get("patientId") == patient_id and prob.get("title") == "Prediabetes":
            target_problem = prob
            break

    if target_problem is None:
        return False, f"Could not find problem 'Prediabetes' for patient Johnson (patientId={patient_id})."

    status = target_problem.get("status", "")
    if status != "Resolved":
        return False, f"Problem 'Prediabetes' status is '{status}', expected 'Resolved'."

    resolved_date = target_problem.get("resolvedDate", "")
    if not resolved_date:
        return False, "Problem 'Prediabetes' has status 'Resolved' but resolvedDate is empty."

    return True, "Successfully verified that Marcus Johnson's 'Prediabetes' is resolved with a resolvedDate set."
