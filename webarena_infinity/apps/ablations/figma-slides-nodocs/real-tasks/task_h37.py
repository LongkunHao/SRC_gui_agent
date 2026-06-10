import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Brand Identity: org→team visibility, disable editing, remove viewers."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    if "pres_002" not in pres_map:
        return False, "pres_002 (Brand Identity Guidelines v2.0) not found."

    p = pres_map["pres_002"]
    ss = p.get("shareSettings", {})
    errors = []

    # Visibility should be team
    vis = ss.get("visibility")
    if vis != "team":
        errors.append(f"visibility is '{vis}', expected 'team'")

    # Editing should be disabled
    if ss.get("allowEditing"):
        errors.append("allowEditing should be false")

    # Viewers (user_005, user_007) should be removed from sharedWith
    viewer_ids = {"user_005", "user_007"}
    shared = set(ss.get("sharedWith", []))
    still_present = viewer_ids & shared
    if still_present:
        errors.append(f"Viewers still in sharedWith: {still_present}")

    # Non-viewers should still be present
    required = {"user_001", "user_002", "user_003", "user_004", "user_006", "user_008"}
    missing = required - shared
    if missing:
        errors.append(f"Non-viewer users missing from sharedWith: {missing}")

    if errors:
        return False, f"pres_002 issues: {'; '.join(errors)}"

    return True, (
        "Brand Identity Guidelines: team visibility, editing disabled, "
        "viewers removed from shared users."
    )
