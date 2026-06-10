import requests
from collections import defaultdict


def verify(server_url: str) -> tuple[bool, str]:
    """Has comment with replies -> star. Has comments but no replies -> unstar."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Classify presentations by reply presence
    has_replies = set()
    has_comments_no_replies = set()
    has_any_comment = set()

    pres_has_reply = defaultdict(bool)
    for c in comments:
        pid = c.get("presentationId")
        has_any_comment.add(pid)
        if c.get("replies") and len(c["replies"]) > 0:
            pres_has_reply[pid] = True

    for pid in has_any_comment:
        if pres_has_reply[pid]:
            has_replies.add(pid)
        else:
            has_comments_no_replies.add(pid)

    # Should be starred (has at least one comment with replies):
    # pres_001,002,004,006,007,010,011,012,013,014,015,016,018
    expected_starred = {
        "pres_001", "pres_002", "pres_004", "pres_006", "pres_007",
        "pres_010", "pres_011", "pres_012", "pres_013", "pres_014",
        "pres_015", "pres_016", "pres_018",
    }
    # Should be unstarred (has comments but none have replies):
    # pres_003, pres_005, pres_008, pres_009
    expected_unstarred = {"pres_003", "pres_005", "pres_008", "pres_009"}

    errors = []

    for pid in expected_starred:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        if not pres_map[pid].get("starred"):
            errors.append(
                f"{pid} ({pres_map[pid].get('title')}): should be starred "
                f"(has comment with replies)"
            )

    for pid in expected_unstarred:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        if pres_map[pid].get("starred"):
            errors.append(
                f"{pid} ({pres_map[pid].get('title')}): should be unstarred "
                f"(comments but no replies)"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "13 presentations with replied comments starred. "
        "4 presentations with reply-less comments unstarred."
    )
