import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Replace Marketing Campaign's shared users with Accessibility Audit's shared users."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    if "pres_010" not in pres_map:
        return False, "pres_010 (Marketing Campaign) not found."

    p = pres_map["pres_010"]
    shared = set(p.get("shareSettings", {}).get("sharedWith", []))

    # pres_011 (Accessibility Audit) sharedWith: [user_001, user_003, user_004]
    required = {"user_001", "user_003", "user_004"}

    missing = required - shared
    if missing:
        return False, (
            f"pres_010 sharedWith missing Accessibility Audit users: {missing}. "
            f"Current: {sorted(shared)}"
        )

    # Original Marketing Campaign users (user_002, user_008) should be removed
    # (user_001 is in both so stays)
    should_not_be_present = {"user_002", "user_008"}
    unwanted = should_not_be_present & shared
    if unwanted:
        return False, (
            f"pres_010 sharedWith still contains original users that aren't in "
            f"Accessibility Audit: {unwanted}. Current: {sorted(shared)}"
        )

    return True, (
        "Marketing Campaign shared users replaced with Accessibility Audit users: "
        "[user_001, user_003, user_004]."
    )
