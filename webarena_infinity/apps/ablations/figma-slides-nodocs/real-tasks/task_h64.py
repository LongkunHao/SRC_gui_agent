import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Editor-created: unresolved comments -> star, all resolved -> archive."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    users = state.get("users", [])
    pres_map = {p["id"]: p for p in presentations}

    editors = {u["id"] for u in users if u.get("role") == "editor"}

    # Categorize comments per presentation
    pres_has_unresolved = set()
    pres_has_any_comment = set()
    pres_all_resolved = set()

    from collections import defaultdict
    resolved_map = defaultdict(lambda: {"resolved": 0, "unresolved": 0})
    for c in comments:
        pid = c["presentationId"]
        pres_has_any_comment.add(pid)
        if c.get("resolved"):
            resolved_map[pid]["resolved"] += 1
        else:
            resolved_map[pid]["unresolved"] += 1
            pres_has_unresolved.add(pid)

    for pid in pres_has_any_comment:
        if pid not in pres_has_unresolved:
            pres_all_resolved.add(pid)

    # Editor-created presentations:
    # Should star (has unresolved): pres_002,004,005,008,010,013,016,018
    # Should archive (all resolved): pres_011,014,015
    should_star = {
        "pres_002", "pres_004", "pres_005", "pres_008",
        "pres_010", "pres_013", "pres_016", "pres_018",
    }
    should_archive = {"pres_011", "pres_014", "pres_015"}

    errors = []

    for pid in should_star:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if not p.get("starred"):
            errors.append(
                f"{pid} ({p.get('title')}): should be starred "
                f"(editor-created with unresolved comments)"
            )

    for pid in should_archive:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if p.get("status") != "archived":
            errors.append(
                f"{pid} ({p.get('title')}): should be archived "
                f"(editor-created, all comments resolved), got status='{p.get('status')}'"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "8 editor-created presentations with unresolved comments starred. "
        "3 editor-created presentations with all-resolved comments archived."
    )
