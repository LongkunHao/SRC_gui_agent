import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify that the patient referred to podiatry for neuropathy screening (Patricia O'Brien, pat_8)
    has a new in-person appointment scheduled with Dr. Chen (prov_1) on April 15, 2026 at 2:00 PM."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    seed_appt_ids = {f"appt_{i}" for i in range(1, 21)}
    appointments = state.get("appointments", [])

    for appt in appointments:
        if appt.get("id") in seed_appt_ids:
            continue
        if (appt.get("patientId") == "pat_8"
                and appt.get("providerId") == "prov_1"
                and appt.get("place") == "in_person"
                and appt.get("status") == "scheduled"
                and "2026-04-15" in appt.get("date", "")
                and "14:00" in appt.get("date", "")):
            return True, "New in-person appointment for pat_8 with prov_1 on 2026-04-15 at 14:00 confirmed"

    new_for_pat8 = [
        a for a in appointments
        if a.get("id") not in seed_appt_ids and a.get("patientId") == "pat_8"
    ]
    if new_for_pat8:
        details = [
            f"id={a.get('id')}, provider={a.get('providerId')}, place={a.get('place')}, "
            f"status={a.get('status')}, date={a.get('date')}"
            for a in new_for_pat8
        ]
        return False, (
            f"Found new appointment(s) for pat_8 but none matched all criteria "
            f"(prov_1, in_person, scheduled, 2026-04-15T14:00). Details: {'; '.join(details)}"
        )

    return False, "No new appointment found for pat_8 (Patricia O'Brien)"
