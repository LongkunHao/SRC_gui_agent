import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Unstar all, then star only where creator commented on own presentation."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Presentations where creator has a comment on it:
    # pres_003: creator user_001, comments cmt_009(user_001) -> YES
    # pres_005: creator user_004, comments cmt_040(user_004) -> YES
    # pres_012: creator user_005, comments cmt_039(user_005) -> YES
    should_star = {"pres_003", "pres_005", "pres_012"}

    errors = []

    for p in presentations:
        pid = p["id"]
        if pid in should_star:
            if not p.get("starred"):
                errors.append(
                    f"{pid} ({p.get('title')}): should be starred "
                    f"(creator commented on own presentation)"
                )
        else:
            if p.get("starred"):
                errors.append(
                    f"{pid} ({p.get('title')}): should NOT be starred"
                )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Only 3 presentations starred (where creator commented on own): "
        "pres_003, pres_005, pres_012. All others unstarred."
    )
