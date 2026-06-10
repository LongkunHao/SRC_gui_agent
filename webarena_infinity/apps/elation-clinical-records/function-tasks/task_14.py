import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Helen Zhao by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Zhao":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Zhao' not found."

    patient_id = patient.get("id")

    # Find problem 'Hypothyroidism' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Hypothyroidism"):
            status = problem.get("status", "")
            resolved_date = problem.get("resolvedDate", "")
            if status == "Resolved" and resolved_date:
                return True, (f"Problem 'Hypothyroidism' for Helen Zhao has status 'Resolved' "
                              f"with resolvedDate '{resolved_date}'.")
            errors = []
            if status != "Resolved":
                errors.append(f"status is '{status}' (expected 'Resolved')")
            if not resolved_date:
                errors.append("resolvedDate is empty (expected non-empty)")
            return False, f"Problem 'Hypothyroidism' for Helen Zhao: {'; '.join(errors)}."

    return False, "Problem 'Hypothyroidism' not found for Helen Zhao."
