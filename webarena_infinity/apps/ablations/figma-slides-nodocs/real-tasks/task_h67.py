import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Delete last slide from presentations with all-resolved comments."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    slides = state.get("slides", [])
    pres_map = {p["id"]: p for p in presentations}

    # Presentations with all comments resolved (>=1 comment, 0 unresolved):
    # pres_011: was 9 slides -> now 8
    # pres_014: was 6 slides -> now 5
    # pres_015: was 11 slides -> now 10
    expected_counts = {
        "pres_011": 8,
        "pres_014": 5,
        "pres_015": 10,
    }

    # Original last-slide IDs that should be deleted
    deleted_slides = {"slide_011_08", "slide_014_05", "slide_015_10"}

    errors = []

    # Check slide counts
    for pid, expected_count in expected_counts.items():
        pres_slides = [s for s in slides if s.get("presentationId") == pid]
        actual_count = len(pres_slides)
        if actual_count != expected_count:
            errors.append(
                f"{pid}: expected {expected_count} slides, got {actual_count}"
            )

        if pid in pres_map:
            sc = pres_map[pid].get("slideCount")
            if sc != expected_count:
                errors.append(
                    f"{pid}: slideCount should be {expected_count}, got {sc}"
                )

    # Check deleted slides are gone
    remaining = [s for s in slides if s.get("id") in deleted_slides]
    if remaining:
        ids = [s.get("id") for s in remaining]
        errors.append(f"Last slides that should be deleted still present: {ids}")

    if errors:
        return False, "; ".join(errors)

    return True, (
        "Last slide deleted from 3 presentations with all-resolved comments: "
        "pres_011 (8 slides), pres_014 (5 slides), pres_015 (10 slides)."
    )
