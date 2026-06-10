import requests
from collections import defaultdict


def verify(server_url: str) -> tuple[bool, str]:
    """Presentations with 3+ unique comment authors: star + org visibility."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    comments = state.get("comments", [])
    pres_map = {p["id"]: p for p in presentations}

    # Count unique authors per presentation
    authors_per_pres = defaultdict(set)
    for c in comments:
        authors_per_pres[c["presentationId"]].add(c["authorId"])

    # Seed presentations with 3+ unique comment authors:
    # pres_001: user_002,003,004,005,006,008 = 6
    # pres_002: user_001,002,003,008 = 4
    # pres_004: user_001,002,004,006 = 4
    # pres_006: user_003,004,005,007,008 = 5
    target_pres = {
        pid for pid, authors in authors_per_pres.items() if len(authors) >= 3
    }
    expected = {"pres_001", "pres_002", "pres_004", "pres_006"}

    errors = []

    if target_pres != expected:
        errors.append(
            f"Expected presentations with 3+ authors: {expected}, "
            f"computed: {target_pres}"
        )

    for pid in expected:
        if pid not in pres_map:
            errors.append(f"{pid} not found")
            continue
        p = pres_map[pid]
        if not p.get("starred"):
            errors.append(f"{pid} ({p.get('title')}): should be starred")
        vis = p.get("shareSettings", {}).get("visibility")
        if vis != "organization":
            errors.append(
                f"{pid} ({p.get('title')}): visibility should be "
                f"'organization', got '{vis}'"
            )

    if errors:
        return False, "; ".join(errors)

    return True, (
        "4 presentations with 3+ unique comment authors are starred "
        "and set to organization visibility."
    )
