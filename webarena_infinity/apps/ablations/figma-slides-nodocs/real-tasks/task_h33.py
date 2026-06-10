import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Create 'All-Team Sync Q2' shared with intersection of Roadmap and Mobile DS users."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])

    match = None
    for p in presentations:
        if p.get("title", "").strip().lower() == "all-team sync q2":
            match = p
            break

    if match is None:
        return False, "No presentation titled 'All-Team Sync Q2' found."

    errors = []

    # Check theme
    theme = match.get("theme")
    if theme != "warm":
        errors.append(f"theme is '{theme}', expected 'warm'")

    # Check tags
    tags = [t.lower() for t in match.get("tags", [])]
    if "team" not in tags:
        errors.append(f"tag 'team' missing from tags: {match.get('tags')}")
    if "sync" not in tags:
        errors.append(f"tag 'sync' missing from tags: {match.get('tags')}")

    # pres_001 sharedWith: [user_002, user_003, user_004]
    # pres_013 sharedWith: [user_001, user_002, user_003, user_004, user_006, user_008]
    # Intersection: [user_002, user_003, user_004]
    # Plus creator user_001
    required_users = {"user_001", "user_002", "user_003", "user_004"}
    shared = set(match.get("shareSettings", {}).get("sharedWith", []))

    missing = required_users - shared
    if missing:
        errors.append(f"sharedWith missing required users: {missing}")

    # Should NOT include users only in one list (user_005, user_006, user_007, user_008)
    # unless they're user_001 (creator). user_006 and user_008 are only in pres_013.
    extra_not_in_intersection = {"user_005", "user_006", "user_007", "user_008"}
    unwanted = extra_not_in_intersection & shared
    if unwanted:
        errors.append(
            f"sharedWith contains users not in the intersection of both presentations: {unwanted}"
        )

    if errors:
        return False, f"'All-Team Sync Q2' issues: {'; '.join(errors)}"

    return True, (
        "'All-Team Sync Q2' created with warm theme, correct tags, "
        "and shared with intersection of Roadmap and Mobile DS users."
    )
