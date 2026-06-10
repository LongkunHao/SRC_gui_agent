import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Resolve comments on Eng Architecture, set org visibility, add Brand Identity users."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    if "pres_005" not in pres_map:
        return False, "pres_005 (Engineering Architecture Overview) not found."

    p = pres_map["pres_005"]
    errors = []

    # All comments on pres_005 should be resolved
    pres_005_comments = [c for c in comments if c.get("presentationId") == "pres_005"]
    unresolved = [c for c in pres_005_comments if not c.get("resolved", False)]
    if unresolved:
        ids = [c.get("id") for c in unresolved]
        errors.append(f"Unresolved comments remain on pres_005: {ids}")

    # Visibility should be organization
    vis = p.get("shareSettings", {}).get("visibility")
    if vis != "organization":
        errors.append(f"visibility is '{vis}', expected 'organization'")

    # Should contain all users from pres_002 (Brand Identity Guidelines)
    # pres_002 sharedWith: all 8 users
    required_users = {
        "user_001", "user_002", "user_003", "user_004",
        "user_005", "user_006", "user_007", "user_008"
    }
    shared = set(p.get("shareSettings", {}).get("sharedWith", []))
    missing = required_users - shared
    if missing:
        errors.append(f"sharedWith missing users from Brand Identity Guidelines: {missing}")

    if errors:
        return False, f"pres_005 issues: {'; '.join(errors)}"

    return True, (
        "Engineering Architecture Overview: all comments resolved, "
        "organization visibility, all Brand Identity users added."
    )
