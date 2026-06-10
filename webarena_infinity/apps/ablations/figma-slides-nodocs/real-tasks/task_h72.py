import requests
from collections import Counter


def verify(server_url: str) -> tuple[bool, str]:
    """Exactly 4 comments: resolve+disable editing+team. Exactly 5: delete resolved+enable editing+star."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Seed comment counts:
    # Exactly 4: pres_002 (cmt_006,007,008,030), pres_004 (cmt_011,012,013,037)
    # Exactly 5: pres_006 (cmt_014,015,016,031,032)
    four_pres = {"pres_002", "pres_004"}
    five_pres = {"pres_006"}

    errors = []

    # Check exactly-4 presentations: all comments resolved, editing disabled, team vis
    for pid in four_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        # All comments should be resolved
        pres_comments = [c for c in comments if c.get("presentationId") == pid]
        unresolved = [c for c in pres_comments if not c.get("resolved")]
        if unresolved:
            ids = [c.get("id") for c in unresolved]
            errors.append(f"{pid}: comments should all be resolved, unresolved: {ids}")

        if ss.get("allowEditing"):
            errors.append(f"{pid}: editing should be disabled")
        if ss.get("visibility") != "team":
            errors.append(
                f"{pid}: visibility should be 'team', got '{ss.get('visibility')}'"
            )

    # Check exactly-5 presentations: resolved comments deleted, editing enabled, starred
    for pid in five_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        # Resolved comments on pres_006: cmt_015, cmt_031 should be deleted
        deleted = {"cmt_015", "cmt_031"}
        remaining_deleted = [
            c for c in comments
            if c.get("id") in deleted
        ]
        if remaining_deleted:
            ids = [c.get("id") for c in remaining_deleted]
            errors.append(f"{pid}: resolved comments should be deleted: {ids}")

        if not ss.get("allowEditing"):
            errors.append(f"{pid}: editing should be enabled")
        if not p.get("starred"):
            errors.append(f"{pid}: should be starred")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Exactly-4-comment presentations: resolved, editing off, team visibility. "
        "Exactly-5-comment presentation: resolved deleted, editing on, starred."
    )
