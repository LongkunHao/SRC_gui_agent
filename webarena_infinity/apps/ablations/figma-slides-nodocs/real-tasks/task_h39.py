import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Create 'Quarterly Design Review' with creative theme, share with Mobile DS non-viewers."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    match = None
    for p in presentations:
        if p.get("title", "").strip().lower() == "quarterly design review":
            match = p
            break

    if match is None:
        return False, "No presentation titled 'Quarterly Design Review' found."

    errors = []

    # Check theme
    theme = match.get("theme")
    if theme != "creative":
        errors.append(f"theme is '{theme}', expected 'creative'")

    # Check tags
    tags = [t.lower() for t in match.get("tags", [])]
    if "design" not in tags:
        errors.append(f"tag 'design' missing from tags: {match.get('tags')}")
    if "review" not in tags:
        errors.append(f"tag 'review' missing from tags: {match.get('tags')}")

    # pres_013 sharedWith: [user_001, user_002, user_003, user_004, user_006, user_008]
    # All are non-viewers (no viewers in pres_013's sharedWith)
    required_users = {"user_001", "user_002", "user_003", "user_004", "user_006", "user_008"}
    viewer_ids = {"user_005", "user_007"}

    shared = set(match.get("shareSettings", {}).get("sharedWith", []))
    missing = required_users - shared
    if missing:
        errors.append(f"sharedWith missing Mobile DS non-viewer users: {missing}")

    # Viewers should not be present
    unwanted = viewer_ids & shared
    if unwanted:
        errors.append(f"Viewers should not be in sharedWith: {unwanted}")

    if errors:
        return False, f"'Quarterly Design Review' issues: {'; '.join(errors)}"

    return True, (
        "'Quarterly Design Review' created with creative theme, correct tags, "
        "and shared with Mobile Design System non-viewer users."
    )
