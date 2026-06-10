import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Marcus Rivera's presentations: unstar starred ones, archive published unstarred ones, leave drafts."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Marcus (user_002) has access to these presentations (in sharedWith)
    # pres_001, pres_002, pres_004, pres_006, pres_008, pres_010, pres_013, pres_014, pres_018

    # Originally starred → should be unstarred
    should_unstar = {"pres_001", "pres_002", "pres_006", "pres_010", "pres_013"}
    # Originally published + unstarred → should be archived
    should_archive = {"pres_004", "pres_008", "pres_014"}
    # Originally draft → should be unchanged
    should_leave = {"pres_018"}

    errors = []

    for pid in should_unstar:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if p.get("starred", False):
            errors.append(f"{pid} ({p.get('title')}) should be unstarred but is still starred")

    for pid in should_archive:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if p.get("status") != "archived":
            errors.append(
                f"{pid} ({p.get('title')}) should be archived but has status='{p.get('status')}'"
            )

    for pid in should_leave:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if p.get("status") != "draft":
            errors.append(
                f"{pid} ({p.get('title')}) is a draft and should be unchanged, "
                f"but has status='{p.get('status')}'"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All Marcus Rivera's presentations handled correctly: "
        "5 unstarred, 3 archived, 1 draft left unchanged."
    )
