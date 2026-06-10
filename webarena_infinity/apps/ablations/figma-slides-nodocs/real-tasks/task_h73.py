import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Sarah commented but not creator: star, enable comments, resolve Sarah's comments."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    sarah = "user_001"

    # Sarah commented on these presentations she didn't create:
    # pres_002 (creator user_006): cmt_006
    # pres_004 (creator user_003): cmt_011
    # pres_010 (creator user_008): cmt_019, cmt_038
    # pres_012 (creator user_005): cmt_022
    # pres_013 (creator user_006): cmt_034
    # pres_015 (creator user_004): cmt_025
    targets = {
        "pres_002": ["cmt_006"],
        "pres_004": ["cmt_011"],
        "pres_010": ["cmt_019", "cmt_038"],
        "pres_012": ["cmt_022"],
        "pres_013": ["cmt_034"],
        "pres_015": ["cmt_025"],
    }

    errors = []

    for pid, sarah_cmt_ids in targets.items():
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        if not p.get("starred"):
            errors.append(f"{pid} ({p.get('title')}): should be starred")

        if not ss.get("allowComments"):
            errors.append(f"{pid} ({p.get('title')}): comments should be enabled")

        # Check Sarah's comments are resolved
        for cmt_id in sarah_cmt_ids:
            cmt = next((c for c in comments if c.get("id") == cmt_id), None)
            if cmt is None:
                errors.append(f"{cmt_id} on {pid}: comment not found")
                continue
            if not cmt.get("resolved"):
                errors.append(
                    f"{cmt_id} on {pid}: Sarah's comment should be resolved"
                )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "6 presentations where Sarah commented (not creator): "
        "all starred, comments enabled, Sarah's comments resolved."
    )
