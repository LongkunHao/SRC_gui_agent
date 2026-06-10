import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Fitzgerald (pat_011)
    patients = state.get("patients", [])
    fitzgerald = None
    for p in patients:
        if p.get("lastName") == "Fitzgerald":
            fitzgerald = p
            break
    if not fitzgerald:
        return False, "Patient with lastName 'Fitzgerald' not found."

    patient_id = fitzgerald.get("id", "pat_011")

    # Find visit note for Fitzgerald with the required properties
    notes = state.get("visitNotes", [])
    matching_notes = []
    for note in notes:
        if note.get("patientId") != patient_id:
            continue
        if (note.get("format") == "pre_op" and
                note.get("category") == "cat_009" and
                note.get("templateUsed") == "tmpl_010" and
                note.get("status") == "signed"):
            matching_notes.append(note)

    if not matching_notes:
        # Provide diagnostics
        fitz_notes = [n for n in notes if n.get("patientId") == patient_id]
        if not fitz_notes:
            return False, "No visit notes found for Fitzgerald."
        details = []
        for n in fitz_notes:
            details.append(
                f"id={n.get('id')}, format={n.get('format')}, "
                f"category={n.get('category')}, templateUsed={n.get('templateUsed')}, "
                f"status={n.get('status')}"
            )
        return False, (
            f"Found {len(fitz_notes)} note(s) for Fitzgerald but none match all criteria "
            f"(format=pre_op, category=cat_009, templateUsed=tmpl_010, status=signed). "
            f"Notes: {'; '.join(details)}"
        )

    return True, "Fitzgerald has a signed visit note with Pre-Op H&P format, Pre-Op Evaluation category, and Pre-Operative Evaluation template."
