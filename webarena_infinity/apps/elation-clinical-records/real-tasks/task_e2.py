import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Nakamura":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Nakamura'."

    patient_id = patient.get("id")
    problems = state.get("problems", [])
    target_problem = None
    for prob in problems:
        if prob.get("patientId") == patient_id and prob.get("title") == "Plantar Fasciitis, Right Foot":
            target_problem = prob
            break

    if target_problem is None:
        return False, f"Could not find problem 'Plantar Fasciitis, Right Foot' for patient Nakamura (patientId={patient_id})."

    status = target_problem.get("status", "")
    if status != "Active":
        return False, f"Problem 'Plantar Fasciitis, Right Foot' status is '{status}', expected 'Active'."

    return True, "Successfully verified that Emily Nakamura's 'Plantar Fasciitis, Right Foot' is marked as Active."
