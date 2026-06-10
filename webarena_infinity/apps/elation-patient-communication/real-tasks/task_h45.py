import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that Howard Blackwell's (pat_27) virtual appointment (appt_9) is cancelled and a new
    in-person appointment exists with the same provider (prov_4) on the same date (2026-03-15)."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    seed_appt_ids = {f"appt_{i}" for i in range(1, 21)}

    appointments = state.get("appointments", [])
    if not appointments:
        return False, "No appointments found in state"

    # Check appt_9 is cancelled
    appt_9 = None
    for appt in appointments:
        if appt.get("id") == "appt_9":
            appt_9 = appt
            break

    if not appt_9:
        return False, "appt_9 not found in state"

    errors = []

    appt_9_status = appt_9.get("status", "")
    if appt_9_status != "cancelled":
        errors.append(f"appt_9 status is '{appt_9_status}', expected 'cancelled'")

    # Look for new in-person appointment for pat_27 with prov_4 on 2026-03-15
    new_appt_found = False
    for appt in appointments:
        appt_id = appt.get("id", "")
        if appt_id in seed_appt_ids:
            continue

        patient_id = appt.get("patientId", "")
        provider_id = appt.get("providerId", "")
        place = appt.get("place", "")
        date = appt.get("date", "")

        if (patient_id == "pat_27" and provider_id == "prov_4"
                and place == "in_person" and "2026-03-15" in date):
            new_appt_found = True
            break

    if not new_appt_found:
        errors.append(
            "No new in-person appointment found for pat_27 with prov_4 on 2026-03-15"
        )

    if errors:
        return False, "; ".join(errors)

    return True, "appt_9 cancelled and new in-person appointment created for pat_27 with prov_4 on 2026-03-15"
