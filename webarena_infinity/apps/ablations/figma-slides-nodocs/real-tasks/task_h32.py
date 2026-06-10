import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Find presentation with most comments, add all comment authors to its shared users."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # pres_001 has 6 comments (most): cmt_001, cmt_002, cmt_003, cmt_004, cmt_005, cmt_029
    # Authors: user_002, user_003, user_004, user_006, user_005, user_008
    target_id = "pres_001"

    if target_id not in pres_map:
        return False, "pres_001 (Q1 2026 Product Roadmap) not found."

    # Verify it still has the most comments
    comment_counts = {}
    for c in comments:
        pid = c.get("presentationId")
        comment_counts[pid] = comment_counts.get(pid, 0) + 1

    max_count = max(comment_counts.values()) if comment_counts else 0
    if comment_counts.get(target_id, 0) != max_count:
        return False, (
            f"pres_001 doesn't have the most comments. "
            f"Counts: {sorted(comment_counts.items(), key=lambda x: -x[1])[:3]}"
        )

    p = pres_map[target_id]
    shared = set(p.get("shareSettings", {}).get("sharedWith", []))

    # All comment authors should be in sharedWith
    required_authors = {"user_002", "user_003", "user_004", "user_005", "user_006", "user_008"}
    missing = required_authors - shared
    if missing:
        return False, (
            f"pres_001 sharedWith missing comment authors: {missing}. "
            f"Current: {sorted(shared)}"
        )

    return True, (
        "Presentation with most comments (pres_001, 6 comments) now has "
        "all comment authors in its shared users."
    )
