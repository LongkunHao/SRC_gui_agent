import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check 1: Category "Chronic Disease Management" exists with countForMIPS=True
    categories = state.get("visitNoteCategories", [])
    cdm_category = None
    for cat in categories:
        name = (cat.get("name") or "").strip()
        if name.lower() == "chronic disease management":
            cdm_category = cat
            break

    if not cdm_category:
        return False, "Category 'Chronic Disease Management' not found."

    if not cdm_category.get("countForMIPS"):
        return False, (
            f"Category 'Chronic Disease Management' found (id={cdm_category.get('id')}) "
            f"but countForMIPS is {cdm_category.get('countForMIPS')}, expected True."
        )

    cdm_id = cdm_category.get("id")

    # Check 2: Follow-Up appointment type uses this category
    appointment_types = state.get("appointmentTypes", [])
    follow_up = None
    for apt in appointment_types:
        name = (apt.get("name") or "").strip()
        if name.lower() == "follow-up" or apt.get("id") == "apt_006":
            follow_up = apt
            break

    if not follow_up:
        return False, "Appointment type 'Follow-Up' not found."

    note_category = follow_up.get("noteCategory")
    if note_category != cdm_id:
        return False, (
            f"Follow-Up appointment noteCategory is '{note_category}', "
            f"expected '{cdm_id}' (Chronic Disease Management)."
        )

    return True, (
        f"Category 'Chronic Disease Management' (id={cdm_id}) exists with MIPS enabled, "
        f"and Follow-Up appointment is set to use it."
    )
