import requests


def verify(server_url: str) -> tuple[bool, str]:
    """For presentations with exactly 1 comment: star if unresolved, delete if resolved."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Presentations with exactly 1 comment in seed data:
    # pres_005: cmt_040 (unresolved) → star
    # pres_008: cmt_018 (unresolved) → star
    # pres_009: cmt_033 (unresolved) → star
    # pres_011: cmt_021 (resolved) → delete comment
    # pres_014: cmt_024 (resolved) → delete comment
    # pres_015: cmt_025 (resolved) → delete comment
    # pres_018: cmt_028 (unresolved) → star

    should_be_starred = {"pres_005", "pres_008", "pres_009", "pres_018"}
    should_delete_comments = {"cmt_021", "cmt_024", "cmt_025"}

    errors = []

    # Check starred
    for pid in should_be_starred:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if not p.get("starred", False):
            errors.append(
                f"{pid} ({p.get('title')}) should be starred but is not"
            )

    # Check deleted comments
    comment_ids = {c.get("id") for c in comments}
    still_present = should_delete_comments & comment_ids
    if still_present:
        errors.append(f"Resolved single-comments should be deleted but still present: {still_present}")

    # Total comments should be 37 (40 - 3 deleted)
    expected_count = 37
    if len(comments) != expected_count:
        errors.append(
            f"Expected {expected_count} comments (40 - 3 deleted), found {len(comments)}"
        )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Single-comment presentations handled: 4 starred (unresolved), "
        "3 resolved comments deleted."
    )
