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
        if prob.get("patientId") == patient_id and prob.get("title") == "Chronic Low Back Pain with Lumbar Disc Degeneration":
            target_problem = prob
            break

    if target_problem is None:
        patient_problems = [prob.get("title") for prob in problems if prob.get("patientId") == patient_id]
        return False, f"Could not find problem titled 'Chronic Low Back Pain with Lumbar Disc Degeneration' for patient Johnson (patientId={patient_id}). Current problems: {patient_problems}"

    return True, "Successfully verified that Johnson's 'Chronic Low Back Pain' was renamed to 'Chronic Low Back Pain with Lumbar Disc Degeneration'."
