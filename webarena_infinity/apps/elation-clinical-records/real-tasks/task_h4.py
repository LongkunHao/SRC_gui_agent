import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Henderson (pat_001)
    patients = state.get("patients", [])
    henderson = None
    for p in patients:
        if p.get("lastName") == "Henderson":
            henderson = p
            break
    if not henderson:
        return False, "Patient with lastName 'Henderson' not found."

    patient_id = henderson.get("id", "pat_001")

    # Find vaccination for Henderson with Shingrix dose 2
    vaccinations = state.get("vaccinations", [])
    henderson_vax = [v for v in vaccinations if v.get("patientId") == patient_id]

    matching = []
    for v in henderson_vax:
        vax_name = (v.get("vaccineName") or "").lower()
        if "shingrix" not in vax_name:
            continue
        # Must be dose 2 (not the existing dose 1 vax_005)
        series = str(v.get("seriesNumber", ""))
        if series != "2":
            continue
        matching.append(v)

    if not matching:
        return False, (
            f"No Shingrix dose 2 vaccination found for Henderson. "
            f"Found {len(henderson_vax)} total vaccination(s)."
        )

    # Check details of the matching vaccination
    errors = []
    vax = matching[0]

    manufacturer = (vax.get("manufacturer") or "").strip()
    if manufacturer != "GlaxoSmithKline":
        errors.append(f"manufacturer: expected 'GlaxoSmithKline', got '{manufacturer}'")

    method = (vax.get("method") or "").strip()
    if "intramuscular" not in method.lower():
        errors.append(f"method: expected 'Intramuscular', got '{method}'")

    site = (vax.get("site") or "").strip()
    if "left" not in site.lower() or "deltoid" not in site.lower():
        errors.append(f"site: expected 'Left Deltoid', got '{site}'")

    recall = (vax.get("recall") or "").strip().lower()
    if "5" not in recall or "year" not in recall:
        errors.append(f"recall: expected '5 years', got '{vax.get('recall')}'")

    if errors:
        return False, f"Shingrix dose 2 found but with issues: {'; '.join(errors)}"

    return True, "Henderson's 2nd Shingrix dose recorded correctly: GlaxoSmithKline, IM left deltoid, dose 2, 5-year recall."
