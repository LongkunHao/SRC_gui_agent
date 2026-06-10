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

    # Find problem 'Plantar Fasciitis, Right Foot' for this patient
    for problem in state.get("problems", []):
        if (problem.get("patientId") == patient_id and
                problem.get("title") == "Plantar Fasciitis, Right Foot"):
            status = problem.get("status", "")
            resolved_date = problem.get("resolvedDate", "")
            if status == "Active" and resolved_date == "":
                return True, ("Problem 'Plantar Fasciitis, Right Foot' for Emily Nakamura has status 'Active' "
                              "and empty resolvedDate.")
            errors = []
            if status != "Active":
                errors.append(f"status is '{status}' (expected 'Active')")
            if resolved_date != "":
                errors.append(f"resolvedDate is '{resolved_date}' (expected empty string)")
            return False, (f"Problem 'Plantar Fasciitis, Right Foot' for Emily Nakamura: {'; '.join(errors)}.")

    return False, "Problem 'Plantar Fasciitis, Right Foot' not found for Emily Nakamura."
