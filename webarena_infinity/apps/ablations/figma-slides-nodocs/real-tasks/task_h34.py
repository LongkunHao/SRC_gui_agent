import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Series B Pitch: team visibility, add all editors, enable comments, editing disabled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    if "pres_003" not in pres_map:
        return False, "pres_003 (Series B Fundraising Pitch) not found."

    p = pres_map["pres_003"]
    ss = p.get("shareSettings", {})
    errors = []

    # Visibility should be team
    vis = ss.get("visibility")
    if vis != "team":
        errors.append(f"visibility is '{vis}', expected 'team'")

    # All editors + owner should be in sharedWith
    # Editors: user_002, user_003, user_004, user_006, user_008
    # Owner (user_001) should also be there
    required = {"user_001", "user_002", "user_003", "user_004", "user_006", "user_008"}
    shared = set(ss.get("sharedWith", []))
    missing = required - shared
    if missing:
        errors.append(f"sharedWith missing editors/owner: {missing}")

    # Comments should be enabled
    if not ss.get("allowComments"):
        errors.append("allowComments should be true")

    # Editing should be disabled
    if ss.get("allowEditing"):
        errors.append("allowEditing should be false (keep disabled)")

    if errors:
        return False, f"pres_003 issues: {'; '.join(errors)}"

    return True, (
        "Series B Fundraising Pitch: team visibility, all editors added, "
        "comments enabled, editing disabled."
    )
