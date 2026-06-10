import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Mobile-tagged: add all editors, org visibility, resolve unresolved comments."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    users = state.get("users", [])
    pres_map = {p["id"]: p for p in presentations}

    editors = {u["id"] for u in users if u.get("role") == "editor"}
    # editors: user_002, user_003, user_004, user_006, user_008

    # Mobile-tagged presentations: pres_004, pres_013
    mobile_pres = {"pres_004", "pres_013"}

    errors = []

    for pid in mobile_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        # Check all editors in shared users
        shared = set(ss.get("sharedWith", []))
        missing = editors - shared
        if missing:
            errors.append(f"{pid}: sharedWith missing editors: {missing}")

        # Check visibility
        if ss.get("visibility") != "organization":
            errors.append(
                f"{pid}: visibility should be 'organization', "
                f"got '{ss.get('visibility')}'"
            )

        # Check all comments resolved
        pres_comments = [c for c in comments if c.get("presentationId") == pid]
        unresolved = [c for c in pres_comments if not c.get("resolved")]
        if unresolved:
            ids = [c.get("id") for c in unresolved]
            errors.append(f"{pid}: unresolved comments remain: {ids}")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Mobile-tagged presentations: all editors added, "
        "organization visibility, all comments resolved."
    )
