import requests


def verify(server_url: str) -> tuple[bool, str]:
    """For presentations tagged 'sprint': disable editing, add Priya, star."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Tagged 'sprint': pres_008 (Design Sprint Week 12 Recap), pres_014 (Team Retro Sprint 47)
    sprint_pres_ids = {"pres_008", "pres_014"}
    priya_id = "user_006"

    errors = []

    for pid in sprint_pres_ids:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue

        p = pres_map[pid]
        title = p.get("title", pid)
        ss = p.get("shareSettings", {})

        # Should be starred
        if not p.get("starred", False):
            errors.append(f"{pid} ({title}): should be starred")

        # Editing should be disabled
        if ss.get("allowEditing"):
            errors.append(f"{pid} ({title}): allowEditing should be false")

        # Priya should be in sharedWith
        shared = set(ss.get("sharedWith", []))
        if priya_id not in shared:
            errors.append(f"{pid} ({title}): Priya (user_006) not in sharedWith")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Both sprint-tagged presentations: editing disabled, "
        "Priya added to shared users, and starred."
    )
