import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Telehealth Preferred tag added to virtual appointment patients who lacked it."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Patients with scheduled virtual appointments who didn't have the tag:
    # pat_27 (Howard Blackwell) - appt_9, virtual
    # pat_30 (Janet Okonkwo) - appt_13, virtual
    need_tag = {"pat_27", "pat_30"}

    missing = []
    for pat in state.get("patients", []):
        if pat.get("id") in need_tag:
            if "Telehealth Preferred" not in pat.get("tags", []):
                name = f"{pat.get('firstName', '')} {pat.get('lastName', '')}"
                missing.append(name)

    if missing:
        return False, (
            f"Patients with virtual appointments still missing 'Telehealth Preferred' tag: "
            f"{', '.join(missing)}"
        )

    # Also verify patients who already had the tag still have it
    already_had = {"pat_4", "pat_29", "pat_40"}
    for pat in state.get("patients", []):
        if pat.get("id") in already_had:
            if "Telehealth Preferred" not in pat.get("tags", []):
                name = f"{pat.get('firstName', '')} {pat.get('lastName', '')}"
                return False, f"{name} lost their 'Telehealth Preferred' tag"

    return True, "Telehealth Preferred tag added to Howard Blackwell and Janet Okonkwo"
