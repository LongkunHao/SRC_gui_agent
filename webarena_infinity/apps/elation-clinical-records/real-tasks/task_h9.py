import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Bergstrom (pat_007)
    patients = state.get("patients", [])
    bergstrom = None
    for p in patients:
        if p.get("lastName") == "Bergstrom":
            bergstrom = p
            break
    if not bergstrom:
        return False, "Patient with lastName 'Bergstrom' not found."

    patient_id = bergstrom.get("id", "pat_007")

    # Find COVID vaccination for Bergstrom
    vaccinations = state.get("vaccinations", [])
    bergstrom_vax = [v for v in vaccinations if v.get("patientId") == patient_id]

    if not bergstrom_vax:
        return False, "No vaccinations found for Bergstrom."

    matching = []
    for v in bergstrom_vax:
        vax_name = (v.get("vaccineName") or "").lower()
        if "covid" in vax_name and "moderna" in vax_name:
            matching.append(v)
        elif "covid" in vax_name:
            # Also check manufacturer
            mfr = (v.get("manufacturer") or "").lower()
            if "moderna" in mfr:
                matching.append(v)

    if not matching:
        return False, f"No COVID-19 Moderna vaccination found for Bergstrom. Found {len(bergstrom_vax)} vaccination(s)."

    errors = []
    vax = matching[0]

    manufacturer = (vax.get("manufacturer") or "").strip()
    if "moderna" not in manufacturer.lower():
        errors.append(f"manufacturer: expected 'Moderna', got '{manufacturer}'")

    series = str(vax.get("seriesNumber", ""))
    if series != "1":
        errors.append(f"seriesNumber: expected '1', got '{series}'")

    method = (vax.get("method") or "").strip()
    if "intramuscular" not in method.lower():
        errors.append(f"method: expected 'Intramuscular', got '{method}'")

    site = (vax.get("site") or "").strip()
    if "right" not in site.lower() or "deltoid" not in site.lower():
        errors.append(f"site: expected 'Right Deltoid', got '{site}'")

    recall = (vax.get("recall") or "").strip().lower()
    if "3" not in recall or "week" not in recall:
        errors.append(f"recall: expected '3 weeks', got '{vax.get('recall')}'")

    funded = (vax.get("fundedBy") or "").strip()
    if "private" not in funded.lower():
        errors.append(f"fundedBy: expected 'Private', got '{funded}'")

    if errors:
        return False, f"COVID-19 Moderna vaccination found but with issues: {'; '.join(errors)}"

    return True, "Bergstrom's COVID-19 Moderna dose 1 recorded correctly: IM right deltoid, 3-week recall, privately funded."
