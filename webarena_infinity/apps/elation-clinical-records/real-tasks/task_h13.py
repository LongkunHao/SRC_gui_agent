import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check 1: Default note format changed to "simple"
    prefs = state.get("providerPreferences", {})
    default_format = prefs.get("defaultNoteFormat", "")
    if default_format != "simple":
        errors.append(
            f"providerPreferences.defaultNoteFormat is '{default_format}', expected 'simple'."
        )

    # Check 2: Visit note exists for Wu (pat_012)
    patients = state.get("patients", [])
    wu = None
    for p in patients:
        if p.get("lastName") == "Wu":
            wu = p
            break
    if not wu:
        errors.append("Patient with lastName 'Wu' not found.")
    else:
        patient_id = wu.get("id", "pat_012")
        notes = state.get("visitNotes", [])
        wu_notes = [n for n in notes if n.get("patientId") == patient_id]
        if not wu_notes:
            errors.append("No visit note found for Mei-Ling Wu.")

    if errors:
        return False, " ".join(errors)

    return True, "Default note format set to 'simple' and a visit note exists for Mei-Ling Wu."
