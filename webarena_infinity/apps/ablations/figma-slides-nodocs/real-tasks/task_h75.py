import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Add Elena to presentations she commented on but doesn't have access to."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    elena = "user_008"

    # Elena commented on these presentations where she wasn't in sharedWith:
    # pres_001 (sharedWith: [002,003,004]): cmt_029 -> add elena
    # pres_009 (sharedWith: [007]): cmt_033 -> add elena
    targets = {"pres_001", "pres_009"}

    errors = []

    for pid in targets:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        shared = set(p.get("shareSettings", {}).get("sharedWith", []))
        if elena not in shared:
            errors.append(
                f"{pid} ({p.get('title')}): Elena (user_008) should be "
                f"in sharedWith but is not"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Elena Voronova added to pres_001 and pres_009 "
        "(presentations she commented on without access)."
    )
