import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Comments by non-shared-users should be removed."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # In seed data, these comments have authors not in sharedWith:
    # cmt_004: user_006 on pres_001 (sharedWith: 002,003,004)
    # cmt_005: user_005 on pres_001 (sharedWith: 002,003,004)
    # cmt_029: user_008 on pres_001 (sharedWith: 002,003,004)
    # cmt_033: user_008 on pres_009 (sharedWith: 007)
    should_be_deleted = {"cmt_004", "cmt_005", "cmt_029", "cmt_033"}

    errors = []

    # Check deleted comments are gone
    remaining = [c for c in comments if c.get("id") in should_be_deleted]
    if remaining:
        ids = [c.get("id") for c in remaining]
        errors.append(f"Comments that should be deleted still present: {ids}")

    # Verify no remaining comment has an author outside its presentation's sharedWith
    for c in comments:
        pid = c.get("presentationId")
        if pid not in pres_map:
            continue
        shared = set(pres_map[pid].get("shareSettings", {}).get("sharedWith", []))
        if c.get("authorId") not in shared:
            errors.append(
                f"{c.get('id')} author {c.get('authorId')} not in "
                f"{pid} sharedWith {shared}"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All comments by non-shared-users removed (4 comments deleted)."
    )
