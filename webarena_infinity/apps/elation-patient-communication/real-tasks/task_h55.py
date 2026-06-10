import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Dr. Torres's uninvited patients are now invited and all his
    invited patients have passport sharing level 3."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    patients = state.get("patients", [])
    patient_map = {p.get("id"): p for p in patients}

    # Previously uninvited Dr. Torres (prov_2) patients that should now be invited
    newly_invited = {"pat_9": "Anthony Petrov", "pat_37": "Jason Liu"}

    not_invited = []
    for pid, name in newly_invited.items():
        pat = patient_map.get(pid)
        if pat is None:
            not_invited.append(f"{name} ({pid}) - not found")
            continue
        if pat.get("passportStatus") != "invited":
            not_invited.append(f"{name} ({pid}) status='{pat.get('passportStatus')}'")

    if not_invited:
        return False, f"Dr. Torres's uninvited patients still not invited: {', '.join(not_invited)}"

    # All Dr. Torres invited patients must have sharing level 3
    all_invited = {
        "pat_5": "Marcus Johnson",
        "pat_9": "Anthony Petrov",
        "pat_13": "William Chang",
        "pat_21": "George Kowalski",
        "pat_37": "Jason Liu",
    }

    wrong_level = []
    for pid, name in all_invited.items():
        pat = patient_map.get(pid)
        if pat is None:
            wrong_level.append(f"{name} ({pid}) - not found")
            continue
        level = pat.get("passportSharingLevel")
        if level != 3:
            wrong_level.append(f"{name} ({pid}) level={level}")

    if wrong_level:
        return False, (
            f"Dr. Torres's invited patients not at sharing level 3: "
            f"{', '.join(wrong_level)}"
        )

    return True, (
        "Dr. Torres's uninvited patients (pat_9, pat_37) now invited and all 5 "
        "invited patients have passport sharing level 3"
    )
