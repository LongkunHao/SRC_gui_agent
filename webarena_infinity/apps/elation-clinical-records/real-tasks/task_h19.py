import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find O'Brien (pat_005)
    patients = state.get("patients", [])
    obrien = None
    for p in patients:
        if p.get("lastName") == "O'Brien" or p.get("lastName") == "O\u2019Brien":
            obrien = p
            break
    if not obrien:
        return False, "Patient with lastName \"O'Brien\" not found."

    patient_id = obrien.get("id", "pat_005")

    # Find visit notes for O'Brien with category cat_005 (Follow-Up)
    notes = state.get("visitNotes", [])
    obrien_followup_notes = [
        n for n in notes
        if n.get("patientId") == patient_id and n.get("category") == "cat_005"
    ]

    if not obrien_followup_notes:
        obrien_notes = [n for n in notes if n.get("patientId") == patient_id]
        if not obrien_notes:
            return False, "No visit notes found for O'Brien."
        categories = [n.get("category") for n in obrien_notes]
        return False, (
            f"No visit note with category 'cat_005' (Follow-Up) found for O'Brien. "
            f"Found {len(obrien_notes)} note(s) with categories: {categories}"
        )

    for note in obrien_followup_notes:
        blocks = note.get("blocks", [])
        block_types = [b.get("type") for b in blocks]
        has_hpi = any(t == "hpi" for t in block_types)
        has_assessment = any(t == "assessment" for t in block_types)

        if has_hpi and has_assessment:
            return True, (
                f"O'Brien has a visit note (id={note.get('id')}) with Follow-Up category (cat_005), "
                f"an HPI block, and an Assessment block."
            )

    # Diagnostics
    details = []
    for note in obrien_followup_notes:
        blocks = note.get("blocks", [])
        block_types = [b.get("type") for b in blocks]
        details.append(f"id={note.get('id')}: blocks={block_types}")
    return False, (
        f"Found {len(obrien_followup_notes)} Follow-Up note(s) for O'Brien but none have "
        f"both HPI and Assessment blocks. Details: {'; '.join(details)}"
    )
