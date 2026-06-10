import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    appointment_types = state.get("appointmentTypes", [])

    # Find Urgent Same-Day (apt_008)
    urgent = None
    for apt in appointment_types:
        name = (apt.get("name") or "").strip()
        if name.lower() == "urgent same-day" or apt.get("id") == "apt_008":
            urgent = apt
            break

    # Find COVID Vaccine (apt_005)
    covid = None
    for apt in appointment_types:
        name = (apt.get("name") or "").strip()
        if name.lower() == "covid vaccine" or apt.get("id") == "apt_005":
            covid = apt
            break

    errors = []

    if not urgent:
        errors.append("Appointment type 'Urgent Same-Day' not found.")
    else:
        template = urgent.get("noteTemplate")
        if template != "tmpl_002":
            errors.append(
                f"Urgent Same-Day noteTemplate is '{template}', expected 'tmpl_002' "
                f"(E&M Problem-Focused)."
            )

    if not covid:
        errors.append("Appointment type 'COVID Vaccine' not found.")
    else:
        fmt = covid.get("noteFormat")
        if fmt != "non_visit":
            errors.append(
                f"COVID Vaccine noteFormat is '{fmt}', expected 'non_visit'."
            )

    if errors:
        return False, " ".join(errors)

    return True, "Urgent Same-Day set to E&M Problem-Focused template (tmpl_002) and COVID Vaccine format set to Non-Visit Note (non_visit)."
