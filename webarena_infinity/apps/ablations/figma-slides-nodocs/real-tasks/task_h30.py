import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Delete every comment made by someone with a viewer role."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    comments = state.get("comments", [])

    # Viewers: user_005 (Yuki Tanaka), user_007 (David Kim)
    # Their comments: cmt_005 (user_005), cmt_015 (user_007),
    #                 cmt_031 (user_005), cmt_039 (user_005)
    viewer_comment_ids = {"cmt_005", "cmt_015", "cmt_031", "cmt_039"}
    viewer_ids = {"user_005", "user_007"}

    # Check by ID
    still_present = {c.get("id") for c in comments} & viewer_comment_ids
    if still_present:
        return False, f"Viewer comments still present (should be deleted): {still_present}"

    # Check by authorId
    viewer_authored = [
        c.get("id", "?") for c in comments
        if c.get("authorId") in viewer_ids
    ]
    if viewer_authored:
        return False, f"Comments by viewers still exist: {viewer_authored}"

    # Should have 36 comments remaining (40 - 4)
    expected = 36
    if len(comments) != expected:
        return False, (
            f"Expected {expected} comments after deleting 4 viewer comments, "
            f"found {len(comments)}."
        )

    return True, "All 4 comments by viewers deleted; 36 comments remain."
