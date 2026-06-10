import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find note_012 (Kowalski's draft)
    notes = state.get("visitNotes", [])
    note_012 = None
    for n in notes:
        if n.get("id") == "note_012":
            note_012 = n
            break

    if not note_012:
        return False, "Note note_012 (Kowalski's draft) not found."

    errors = []

    # Check blocks for PE and ROS
    blocks = note_012.get("blocks", [])
    block_types = [b.get("type") for b in blocks]

    has_pe = any(t in ("pe", "physicalExam", "physical_exam", "physicalexam") for t in block_types)
    has_ros = any(t in ("ros", "reviewOfSystems", "review_of_systems") for t in block_types)

    if not has_pe:
        errors.append(f"Missing PE block. Block types present: {block_types}")
    if not has_ros:
        errors.append(f"Missing ROS block. Block types present: {block_types}")

    # Check billing items for 99214
    billing_items = note_012.get("billingItems", [])
    cpt_codes = [str(bi.get("cptCode", "")) for bi in billing_items]
    has_99214 = "99214" in cpt_codes
    if not has_99214:
        errors.append(f"Missing billing code 99214. CPT codes present: {cpt_codes}")

    # Check status is signed
    status = note_012.get("status")
    if status != "signed":
        errors.append(f"Status is '{status}', expected 'signed'")

    if errors:
        return False, f"Note note_012 issues: {'; '.join(errors)}"

    return True, "Kowalski's draft (note_012) completed: has PE block, ROS block, billing 99214, and is signed."
