import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Priya Sharma
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Sharma":
            patient = p
            break

    if not patient:
        return False, "Patient 'Sharma' not found."

    patient_id = patient["id"]
    errors = []

    # Find vaccination matching Hepatitis A criteria
    found = False
    for vax in state.get("vaccinations", []):
        if vax.get("patientId") != patient_id:
            continue
        if "Hepatitis A" not in vax.get("vaccineName", ""):
            continue

        found = True
        if vax.get("manufacturer") != "Merck":
            errors.append(f"manufacturer: expected 'Merck', got '{vax.get('manufacturer')}'")
        if vax.get("lotNumber") != "HA-7721":
            errors.append(f"lotNumber: expected 'HA-7721', got '{vax.get('lotNumber')}'")
        if vax.get("method") != "Subcutaneous":
            errors.append(f"method: expected 'Subcutaneous', got '{vax.get('method')}'")
        if vax.get("site") != "Left Upper Arm":
            errors.append(f"site: expected 'Left Upper Arm', got '{vax.get('site')}'")
        if str(vax.get("seriesNumber", "")) != "1":
            errors.append(f"seriesNumber: expected '1', got '{vax.get('seriesNumber')}'")
        if vax.get("recall") != "6 months":
            errors.append(f"recall: expected '6 months', got '{vax.get('recall')}'")
        if vax.get("fundedBy") != "Insurance":
            errors.append(f"fundedBy: expected 'Insurance', got '{vax.get('fundedBy')}'")

        if errors:
            return False, f"Hepatitis A vaccine found but has issues: {'; '.join(errors)}"
        return True, "Hepatitis A vaccine for Priya Sharma recorded with all correct fields."

    if not found:
        return False, "No Hepatitis A vaccination found for Priya Sharma."
