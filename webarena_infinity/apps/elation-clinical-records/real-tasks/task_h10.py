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

    # Find new visit notes for Henderson (exclude existing ones)
    existing_note_ids = {"note_001", "note_002", "note_003", "note_hist_001"}
    notes = state.get("visitNotes", [])
    henderson_new_notes = [
        n for n in notes
        if n.get("patientId") == patient_id and n.get("id") not in existing_note_ids
    ]

    if not henderson_new_notes:
        return False, "No new visit note found for Henderson (existing notes excluded)."

    for note in henderson_new_notes:
        template_used = note.get("templateUsed")
        if template_used != "tmpl_006":
            continue

        blocks = note.get("blocks", [])
        has_care_plan = any(
            b.get("type") in ("carePlan", "care_plan", "careplan")
            for b in blocks
        )
        if has_care_plan:
            return True, (
                f"Henderson has a new note (id={note.get('id')}) with Diabetes Management "
                f"template (tmpl_006) and a Care Plan block."
            )

    # Diagnostics
    details = []
    for note in henderson_new_notes:
        blocks = note.get("blocks", [])
        block_types = [b.get("type") for b in blocks]
        details.append(
            f"id={note.get('id')}: templateUsed={note.get('templateUsed')}, blocks={block_types}"
        )
    return False, (
        f"Found {len(henderson_new_notes)} new note(s) for Henderson but none have "
        f"templateUsed=tmpl_006 with a carePlan block. Details: {'; '.join(details)}"
    )
