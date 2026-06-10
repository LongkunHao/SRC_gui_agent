import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Create 'Onboarding Feedback Q1' with ocean theme, share with All-Hands users minus viewers."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    # Find the new presentation
    match = None
    for p in presentations:
        if p.get("title", "").strip().lower() == "onboarding feedback q1":
            match = p
            break

    if match is None:
        return False, "No presentation titled 'Onboarding Feedback Q1' found."

    errors = []

    # Check theme
    theme = match.get("theme")
    if theme != "ocean":
        errors.append(f"theme is '{theme}', expected 'ocean'")

    # Check tags
    tags = [t.lower() for t in match.get("tags", [])]
    if "onboarding" not in tags:
        errors.append(f"tag 'onboarding' missing from tags: {match.get('tags')}")
    if "feedback" not in tags:
        errors.append(f"tag 'feedback' missing from tags: {match.get('tags')}")

    # Should be shared with All-Hands (pres_006) users except viewers
    # pres_006 sharedWith: all 8 users. Viewers: user_005, user_007
    # Required: user_001, user_002, user_003, user_004, user_006, user_008
    required_users = {"user_001", "user_002", "user_003", "user_004", "user_006", "user_008"}
    viewer_ids = {"user_005", "user_007"}

    shared = set(match.get("shareSettings", {}).get("sharedWith", []))
    missing = required_users - shared
    if missing:
        errors.append(f"sharedWith missing non-viewer All-Hands users: {missing}")

    # Viewers should NOT be in sharedWith
    unwanted = viewer_ids & shared
    if unwanted:
        errors.append(f"Viewers should not be shared: {unwanted}")

    if errors:
        return False, f"'Onboarding Feedback Q1' issues: {'; '.join(errors)}"

    return True, (
        "'Onboarding Feedback Q1' created with ocean theme, correct tags, "
        "and shared with All-Hands non-viewer users."
    )
