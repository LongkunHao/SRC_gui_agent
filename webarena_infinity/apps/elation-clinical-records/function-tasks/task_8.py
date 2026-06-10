import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Emily Nakamura by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Nakamura":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Nakamura' not found."

    patient_id = patient.get("id")

    # Find problem 'Generalized Anxiety Disorder' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Generalized Anxiety Disorder"):
            status = problem.get("status", "")
            resolved_date = problem.get("resolvedDate", "")
            if status == "Resolved" and resolved_date:
                return True, (f"Problem 'Generalized Anxiety Disorder' for Emily Nakamura has status 'Resolved' "
                              f"with resolvedDate '{resolved_date}'.")
            errors = []
            if status != "Resolved":
                errors.append(f"status is '{status}' (expected 'Resolved')")
            if not resolved_date:
                errors.append("resolvedDate is empty (expected non-empty)")
            return False, (f"Problem 'Generalized Anxiety Disorder' for Emily Nakamura: {'; '.join(errors)}.")

    return False, "Problem 'Generalized Anxiety Disorder' not found for Emily Nakamura."
