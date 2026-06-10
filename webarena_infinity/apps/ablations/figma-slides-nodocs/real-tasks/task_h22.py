import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Share the presentation with fewest slides with everyone from the one with most slides."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # Fewest slides: pres_018 (5), Most slides: pres_013 (25)
    fewest_id = "pres_018"
    most_id = "pres_013"

    if fewest_id not in pres_map:
        return False, "pres_018 (Design Workshop Materials) not found."
    if most_id not in pres_map:
        return False, "pres_013 (Mobile Design System Components) not found."

    # pres_013 sharedWith: [user_001, user_002, user_003, user_004, user_006, user_008]
    most_shared = set(pres_map[most_id].get("shareSettings", {}).get("sharedWith", []))
    fewest_shared = set(pres_map[fewest_id].get("shareSettings", {}).get("sharedWith", []))

    required_users = {"user_001", "user_002", "user_003", "user_004", "user_006", "user_008"}
    missing = required_users - fewest_shared
    if missing:
        return False, (
            f"pres_018 sharedWith is missing users from pres_013: {missing}. "
            f"Current sharedWith: {sorted(fewest_shared)}"
        )

    return True, (
        "Presentation with fewest slides (pres_018) now shared with everyone "
        "from the one with most slides (pres_013)."
    )
