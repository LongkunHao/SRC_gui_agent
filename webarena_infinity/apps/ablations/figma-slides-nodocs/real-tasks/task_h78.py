import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Published with only creator in shared: add editors, team vis, enable comments."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    users = state.get("users", [])
    pres_map = {p["id"]: p for p in presentations}

    editors = {u["id"] for u in users if u.get("role") == "editor"}
    # editors: user_002, user_003, user_004, user_006, user_008

    # Published presentations where sharedWith == [creator]:
    # pres_003: published, creator user_001, sharedWith [user_001]
    # pres_009: published, creator user_007, sharedWith [user_007]
    targets = {"pres_003", "pres_009"}

    errors = []

    for pid in targets:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        # Check editors are in shared
        shared = set(ss.get("sharedWith", []))
        missing = editors - shared
        if missing:
            errors.append(f"{pid}: sharedWith missing editors: {missing}")

        if ss.get("visibility") != "team":
            errors.append(
                f"{pid}: visibility should be 'team', got '{ss.get('visibility')}'"
            )

        if not ss.get("allowComments"):
            errors.append(f"{pid}: comments should be enabled")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "2 published presentations with only-creator sharing: "
        "editors added, team visibility, comments enabled."
    )
