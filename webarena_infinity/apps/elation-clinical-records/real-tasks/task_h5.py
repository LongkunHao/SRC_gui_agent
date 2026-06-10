import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Johnson (pat_003)
    patients = state.get("patients", [])
    johnson = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            johnson = p
            break
    if not johnson:
        return False, "Patient with lastName 'Johnson' not found."

    patient_id = johnson.get("id", "pat_003")

    # Find visit notes for Johnson, excluding existing notes
    existing_note_ids = {"note_005", "note_006"}
    notes = state.get("visitNotes", [])
    johnson_new_notes = [
        n for n in notes
        if n.get("patientId") == patient_id and n.get("id") not in existing_note_ids
    ]

    if not johnson_new_notes:
        return False, "No new visit note found for Johnson (existing notes note_005, note_006 excluded)."

    # Check each new note for assessment block and billing 99214
    for note in johnson_new_notes:
        blocks = note.get("blocks", [])
        has_assessment = any(b.get("type") == "assessment" for b in blocks)

        billing_items = note.get("billingItems", [])
        has_99214 = any(str(bi.get("cptCode")) == "99214" for bi in billing_items)

        if has_assessment and has_99214:
            return True, (
                f"New note for Johnson (id={note.get('id')}) has an Assessment block "
                f"and billing code 99214."
            )

    # Diagnostics
    details = []
    for note in johnson_new_notes:
        blocks = note.get("blocks", [])
        block_types = [b.get("type") for b in blocks]
        billing_items = note.get("billingItems", [])
        cpt_codes = [bi.get("cptCode") for bi in billing_items]
        details.append(
            f"id={note.get('id')}: blocks={block_types}, cptCodes={cpt_codes}"
        )

    return False, (
        f"Found {len(johnson_new_notes)} new note(s) for Johnson but none have both "
        f"an assessment block and billing 99214. Details: {'; '.join(details)}"
    )
