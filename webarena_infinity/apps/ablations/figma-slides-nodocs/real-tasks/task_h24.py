import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Both client-tagged presentations: team vis, comments on, editing off, copy older's users to newer."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    pres_map = {p["id"]: p for p in presentations}

    # pres_007 (older, 2026-03-01): Client Proposal — TechVentures Redesign
    # pres_016 (newer, 2026-03-08): Website Redesign Proposal — TechStartup.io
    older_id = "pres_007"
    newer_id = "pres_016"

    for pid in [older_id, newer_id]:
        if pid not in pres_map:
            return False, f"{pid} not found in state."

    errors = []

    # Both should have: team visibility, comments enabled, editing disabled
    for pid in [older_id, newer_id]:
        p = pres_map[pid]
        title = p.get("title", pid)
        ss = p.get("shareSettings", {})

        vis = ss.get("visibility")
        if vis != "team":
            errors.append(f"{pid} ({title}): visibility is '{vis}', expected 'team'")

        if not ss.get("allowComments"):
            errors.append(f"{pid} ({title}): allowComments is not true")

        if ss.get("allowEditing"):
            errors.append(f"{pid} ({title}): allowEditing should be false")

    # Newer (pres_016) should contain all users from older (pres_007)
    # pres_007 original sharedWith: [user_001, user_003, user_007, user_008]
    required_in_newer = {"user_001", "user_003", "user_007", "user_008"}
    newer_shared = set(pres_map[newer_id].get("shareSettings", {}).get("sharedWith", []))

    missing = required_in_newer - newer_shared
    if missing:
        errors.append(
            f"pres_016 sharedWith missing users from pres_007: {missing}. "
            f"Current: {sorted(newer_shared)}"
        )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Both client proposals have team visibility, comments enabled, editing disabled. "
        "Older proposal's shared users copied to newer proposal."
    )
