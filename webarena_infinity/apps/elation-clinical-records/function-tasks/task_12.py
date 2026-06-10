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

    # Get all problem titles for this patient
    patient_problems = [prob for prob in state.get("problems", []) if prob.get("patientId") == patient_id]
    patient_problem_titles = [prob.get("title", "") for prob in patient_problems]

    has_renamed = "Chronic Low Back Pain with Lumbar Disc Degeneration" in patient_problem_titles
    has_old = "Chronic Low Back Pain" in patient_problem_titles

    if has_renamed and not has_old:
        return True, ("Problem 'Chronic Low Back Pain with Lumbar Disc Degeneration' exists and "
                      "'Chronic Low Back Pain' does not exist for Marcus Johnson.")

    errors = []
    if not has_renamed:
        errors.append("'Chronic Low Back Pain with Lumbar Disc Degeneration' not found")
    if has_old:
        errors.append("'Chronic Low Back Pain' still exists (should have been renamed)")

    return False, f"Marcus Johnson's problems: {'; '.join(errors)}. Current titles: {patient_problem_titles}"
