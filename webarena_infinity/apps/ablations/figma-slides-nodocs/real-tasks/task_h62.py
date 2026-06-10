import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Two earliest-created presentations: private, only creator in shared, unstarred."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    # The two earliest-created presentations by createdAt:
    # pres_013: 2025-10-01 (Mobile Design System Components, creator user_006)
    # pres_009: 2025-11-15 (Onboarding Training Module, creator user_007)
    targets = {
        "pres_013": "user_006",
        "pres_009": "user_007",
    }

    pres_map = {p["id"]: p for p in presentations}
    errors = []

    for pid, creator_id in targets.items():
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})

        if p.get("starred"):
            errors.append(f"{pid} ({p.get('title')}): should not be starred")

        if ss.get("visibility") != "private":
            errors.append(
                f"{pid} ({p.get('title')}): visibility should be 'private', "
                f"got '{ss.get('visibility')}'"
            )

        shared = set(ss.get("sharedWith", []))
        expected_shared = {creator_id}
        if shared != expected_shared:
            extra = shared - expected_shared
            missing = expected_shared - shared
            parts = []
            if extra:
                parts.append(f"unexpected users: {extra}")
            if missing:
                parts.append(f"missing creator: {missing}")
            errors.append(
                f"{pid} ({p.get('title')}): sharedWith should be exactly "
                f"{expected_shared}: {'; '.join(parts)}"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Two earliest-created presentations set to private, "
        "shared only with their creators, and unstarred."
    )
