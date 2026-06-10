import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Delete resolved comments, then disable comments on presentations with none remaining."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    errors = []

    # No resolved comments should remain
    resolved = [c for c in comments if c.get("resolved", False)]
    if resolved:
        ids = [c.get("id") for c in resolved]
        errors.append(f"Resolved comments still present: {ids}")

    # Should have 30 comments remaining (40 - 10 resolved)
    if len(comments) != 30:
        errors.append(f"Expected 30 comments after deleting 10 resolved, found {len(comments)}")

    # Presentations that should have 0 comments after deletion:
    # pres_011 (had cmt_021 resolved), pres_014 (had cmt_024 resolved),
    # pres_015 (had cmt_025 resolved), pres_017 (had no comments)
    # These should have allowComments == false
    no_comment_pres = {"pres_011", "pres_014", "pres_015", "pres_017"}

    for pid in no_comment_pres:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        allow = p.get("shareSettings", {}).get("allowComments")
        if allow is not False and allow != 0:
            errors.append(
                f"{pid} ({p.get('title')}): has no comments remaining but "
                f"allowComments is {allow!r}, expected false"
            )

    # Presentations that still have comments should NOT have allowComments changed
    # (verify a sample of presentations that should still allow comments)
    has_comments = {"pres_001", "pres_002", "pres_004", "pres_006", "pres_010"}
    for pid in has_comments:
        if pid in pres_map:
            p = pres_map[pid]
            # These originally had allowComments=true and still have comments
            if not p.get("shareSettings", {}).get("allowComments"):
                errors.append(
                    f"{pid} ({p.get('title')}): still has comments but "
                    f"allowComments was incorrectly disabled"
                )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "All 10 resolved comments deleted. Comments disabled on 4 presentations "
        "with no remaining comments."
    )
