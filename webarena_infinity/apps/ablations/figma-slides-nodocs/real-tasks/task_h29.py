import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Find Yuki Tanaka's published presentation, resolve its comments, archive it."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Yuki Tanaka (user_005) created pres_012 (published) and pres_017 (archived)
    # The published one is pres_012 (Q4 2025 Revenue Analysis)
    target_id = "pres_012"

    if target_id not in pres_map:
        return False, "pres_012 (Q4 2025 Revenue Analysis) not found."

    p = pres_map[target_id]
    errors = []

    # Should be archived
    if p.get("status") != "archived":
        errors.append(f"status is '{p.get('status')}', expected 'archived'")

    # All comments on pres_012 should be resolved
    pres_012_comments = [c for c in comments if c.get("presentationId") == target_id]
    unresolved = [c for c in pres_012_comments if not c.get("resolved", False)]
    if unresolved:
        ids = [c.get("id") for c in unresolved]
        errors.append(f"Unresolved comments remain on pres_012: {ids}")

    if errors:
        return False, f"pres_012 issues: {'; '.join(errors)}"

    return True, (
        "Yuki Tanaka's published presentation (pres_012) has all comments "
        "resolved and is archived."
    )
