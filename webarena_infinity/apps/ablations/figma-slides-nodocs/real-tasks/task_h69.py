import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Share James O'Brien's presentations with all of Anika Patel's shared users."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # James O'Brien (user_004) created: pres_005, pres_015, pres_016
    # Anika Patel (user_003) created: pres_004, pres_011, pres_018
    # Union of Anika's sharedWith:
    #   pres_004: [001,002,004,006]
    #   pres_011: [001,003,004]
    #   pres_018: [002,003]
    #   Union: {001, 002, 003, 004, 006}
    anika_users = {"user_001", "user_002", "user_003", "user_004", "user_006"}
    james_pres = ["pres_005", "pres_015", "pres_016"]

    errors = []

    for pid in james_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        shared = set(p.get("shareSettings", {}).get("sharedWith", []))
        missing = anika_users - shared
        if missing:
            errors.append(
                f"{pid} ({p.get('title')}): sharedWith missing users: {missing}"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All James O'Brien's presentations now shared with all users "
        "from Anika Patel's presentations."
    )
