import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Dr. Sarah Chen = prov_001
    # Patients with primaryProvider=prov_001: Henderson, Nakamura, Rodriguez-Martinez, Bergstrom, Zhao
    target_last_names = ["Henderson", "Nakamura", "Rodriguez-Martinez", "Bergstrom", "Zhao"]

    patients = state.get("patients", [])

    missing = []
    not_found = []

    for last_name in target_last_names:
        patient = None
        for p in patients:
            if p.get("lastName") == last_name:
                patient = p
                break
        if not patient:
            not_found.append(last_name)
            continue

        # Verify primaryProvider is prov_001
        if patient.get("primaryProvider") != "prov_001":
            # Still check tags, the task is about Dr. Chen's patients
            pass

        tags = patient.get("tags", [])
        if "Flu-Season" not in tags:
            missing.append(f"{last_name} (tags: {tags})")

    if not_found:
        return False, f"Patients not found: {', '.join(not_found)}"

    if missing:
        return False, f"The following Dr. Chen patients are missing 'Flu-Season' tag: {', '.join(missing)}"

    return True, "All 5 of Dr. Sarah Chen's patients (Henderson, Nakamura, Rodriguez-Martinez, Bergstrom, Zhao) have the 'Flu-Season' tag."
