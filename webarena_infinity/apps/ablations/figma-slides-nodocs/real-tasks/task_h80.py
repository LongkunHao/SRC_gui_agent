import requests


def verify(server_url: str) -> tuple[bool, str]:
    """David Kim's non-created access: remove him, add Marcus, disable editing."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    david = "user_007"
    marcus = "user_002"

    # David Kim (user_007) in sharedWith but NOT creator:
    # pres_002: creator user_006, sharedWith had user_007
    # pres_006: creator user_001, sharedWith had user_007
    # pres_007: creator user_001, sharedWith had user_007
    # (pres_009: creator IS user_007, skip)
    targets = {"pres_002", "pres_006", "pres_007"}

    errors = []

    for pid in targets:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        ss = p.get("shareSettings", {})
        shared = set(ss.get("sharedWith", []))

        if david in shared:
            errors.append(
                f"{pid} ({p.get('title')}): David Kim (user_007) should be "
                f"removed from sharedWith"
            )

        if marcus not in shared:
            errors.append(
                f"{pid} ({p.get('title')}): Marcus Rivera (user_002) should be "
                f"in sharedWith"
            )

        if ss.get("allowEditing"):
            errors.append(
                f"{pid} ({p.get('title')}): editing should be disabled"
            )

    # Verify David is still in pres_009 (his own creation)
    if "pres_009" in pres_map:
        shared_009 = set(
            pres_map["pres_009"].get("shareSettings", {}).get("sharedWith", [])
        )
        if david not in shared_009:
            errors.append(
                "pres_009: David Kim should still be in sharedWith "
                "(he's the creator)"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "David Kim removed and Marcus Rivera added to 3 presentations "
        "(pres_002, pres_006, pres_007). Editing disabled on all 3."
    )
