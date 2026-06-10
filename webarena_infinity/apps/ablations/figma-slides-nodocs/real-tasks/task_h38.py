import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Star every published presentation created by an editor with team visibility."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Editors: user_002, user_003, user_004, user_006, user_008
    # Published + team visibility + created by editor:
    # pres_004 (user_003), pres_005 (user_004), pres_008 (user_002),
    # pres_010 (user_008), pres_011 (user_003), pres_014 (user_002),
    # pres_015 (user_004)
    should_be_starred = {
        "pres_004", "pres_005", "pres_008", "pres_010",
        "pres_011", "pres_014", "pres_015"
    }

    errors = []
    for pid in should_be_starred:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if not p.get("starred", False):
            errors.append(f"{pid} ({p.get('title')}) should be starred but is not")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All 7 published presentations by editors with team visibility are starred."
    )
