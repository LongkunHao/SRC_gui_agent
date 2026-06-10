import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Build sets of commenters by resolved status
    has_unresolved = set()
    has_comment = set()
    for c in state.get("comments", []):
        has_comment.add(c.get("userId"))
        if c.get("resolved") is not True:
            has_unresolved.add(c.get("userId"))

    resolved_only = has_comment - has_unresolved

    # In seed: unresolved commenters: user_002 (Marcus), user_003 (Aiko),
    # user_004 (James), user_007 (Elena) -> #F24E1E
    # Resolved-only: user_005 (Priya), user_008 (David) -> #0ACF83
    # No comments: user_006 (Tom) -> unchanged

    for c in state.get("collaborators", []):
        uid = c.get("id")
        name = c.get("name")
        color = c.get("avatarColor", "")

        if uid in has_unresolved:
            if color.upper() != "#F24E1E":
                errors.append(
                    f"{name} avatarColor is '{color}', expected '#F24E1E' "
                    f"(has unresolved comment)"
                )
        elif uid in resolved_only:
            if color.upper() != "#0ACF83":
                errors.append(
                    f"{name} avatarColor is '{color}', expected '#0ACF83' "
                    f"(comments all resolved)"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Collaborator avatar colors updated based on comment status"
