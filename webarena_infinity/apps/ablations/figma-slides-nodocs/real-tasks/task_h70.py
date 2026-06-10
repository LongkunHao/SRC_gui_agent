import requests


def verify(server_url: str) -> tuple[bool, str]:
    """>12 slides: published -> org vis + enable comments; draft -> publish + star."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Presentations with > 12 slides:
    # Published: pres_001(15), pres_002(18), pres_004(16), pres_006(21),
    #            pres_007(14), pres_009(16), pres_012(13), pres_013(25)
    # Draft: pres_016(14)
    published_targets = [
        "pres_001", "pres_002", "pres_004", "pres_006",
        "pres_007", "pres_009", "pres_012", "pres_013",
    ]
    draft_targets = ["pres_016"]

    errors = []

    for pid in published_targets:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})
        if ss.get("visibility") != "organization":
            errors.append(
                f"{pid} ({p.get('title')}): visibility should be 'organization', "
                f"got '{ss.get('visibility')}'"
            )
        if not ss.get("allowComments"):
            errors.append(
                f"{pid} ({p.get('title')}): comments should be enabled"
            )

    for pid in draft_targets:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if p.get("status") != "published":
            errors.append(
                f"{pid} ({p.get('title')}): should be published, "
                f"got '{p.get('status')}'"
            )
        if not p.get("starred"):
            errors.append(
                f"{pid} ({p.get('title')}): should be starred"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "8 published presentations with >12 slides set to organization/comments. "
        "1 draft presentation with >12 slides published and starred."
    )
