import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Nature theme: star fewest slides, archive most, delete comments on middle."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Nature theme presentations:
    # pres_004: 16 slides (most) -> archive
    # pres_007: 14 slides (middle) -> delete all comments
    # pres_011: 9 slides (fewest) -> star
    errors = []

    # Check pres_011 is starred
    if "pres_011" in pres_map:
        if not pres_map["pres_011"].get("starred"):
            errors.append("pres_011 (Accessibility Audit, fewest slides): should be starred")
    else:
        errors.append("pres_011 not found")

    # Check pres_004 is archived
    if "pres_004" in pres_map:
        if pres_map["pres_004"].get("status") != "archived":
            errors.append(
                f"pres_004 (User Research, most slides): should be archived, "
                f"got '{pres_map['pres_004'].get('status')}'"
            )
    else:
        errors.append("pres_004 not found")

    # Check pres_007 has no comments
    remaining = [c for c in comments if c.get("presentationId") == "pres_007"]
    if remaining:
        ids = [c.get("id") for c in remaining]
        errors.append(
            f"pres_007 (TechVentures, middle) should have no comments, "
            f"but found: {ids}"
        )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Nature theme: pres_011 starred (fewest slides), "
        "pres_004 archived (most), pres_007 comments deleted (middle)."
    )
