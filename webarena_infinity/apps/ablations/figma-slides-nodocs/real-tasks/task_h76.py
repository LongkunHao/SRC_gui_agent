import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Viewer-creator -> disable comments+editing. Owner-creator -> enable both."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    users = state.get("users", [])
    user_roles = {u["id"]: u.get("role") for u in users}

    # Viewer-created: pres_009 (user_007), pres_012 (user_005), pres_017 (user_005)
    # Owner-created: pres_001 (user_001), pres_003 (user_001), pres_006 (user_001), pres_007 (user_001)
    viewer_pres = {"pres_009", "pres_012", "pres_017"}
    owner_pres = {"pres_001", "pres_003", "pres_006", "pres_007"}

    pres_map = {p["id"]: p for p in presentations}
    errors = []

    for pid in viewer_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})
        if ss.get("allowComments"):
            errors.append(
                f"{pid} ({p.get('title')}): comments should be disabled "
                f"(viewer-created)"
            )
        if ss.get("allowEditing"):
            errors.append(
                f"{pid} ({p.get('title')}): editing should be disabled "
                f"(viewer-created)"
            )

    for pid in owner_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})
        if not ss.get("allowComments"):
            errors.append(
                f"{pid} ({p.get('title')}): comments should be enabled "
                f"(owner-created)"
            )
        if not ss.get("allowEditing"):
            errors.append(
                f"{pid} ({p.get('title')}): editing should be enabled "
                f"(owner-created)"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "3 viewer-created presentations: comments+editing disabled. "
        "4 owner-created presentations: comments+editing enabled."
    )
