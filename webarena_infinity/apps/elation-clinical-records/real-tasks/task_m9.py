import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Henderson":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Henderson'."

    patient_id = patient.get("id")
    problems = state.get("problems", [])
    target_problem = None
    for prob in problems:
        if prob.get("patientId") == patient_id and "diabetes" in prob.get("title", "").lower():
            target_problem = prob
            break

    if target_problem is None:
        patient_problems = [prob.get("title") for prob in problems if prob.get("patientId") == patient_id]
        return False, f"Could not find a diabetes problem for patient Henderson (patientId={patient_id}). Current problems: {patient_problems}"

    synopsis = target_problem.get("synopsis", "")
    if "6.8" not in synopsis:
        return False, f"Diabetes problem synopsis does not contain '6.8'. Current synopsis: '{synopsis}'"

    return True, "Successfully verified that Henderson's diabetes synopsis was updated to reflect A1C 6.8%."
