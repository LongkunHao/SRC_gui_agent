import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Draft presentations: transitions set to none/0, speaker notes cleared."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to get state: {resp.status_code}"

    state = resp.json()
    presentations = state.get("presentations", [])
    slides = state.get("slides", [])

    # Draft presentations in seed: pres_016, pres_018
    draft_pids = {p["id"] for p in presentations if p.get("status") == "draft"}
    expected_drafts = {"pres_016", "pres_018"}

    errors = []

    for pid in expected_drafts:
        pres_slides = [s for s in slides if s.get("presentationId") == pid]
        if not pres_slides:
            errors.append(f"No slides found for {pid}")
            continue

        for s in pres_slides:
            sid = s.get("id")
            t = s.get("transition", {})
            if t.get("type") != "none":
                errors.append(
                    f"{sid}: transition type should be 'none', got '{t.get('type')}'"
                )
            if t.get("duration") != 0:
                errors.append(
                    f"{sid}: transition duration should be 0, got {t.get('duration')}"
                )
            notes = s.get("speakerNotes", "")
            if notes:
                errors.append(
                    f"{sid}: speaker notes should be empty, got '{notes[:50]}...'"
                )

    if errors:
        return False, "; ".join(errors[:8])

    return True, (
        "All slides on draft presentations have transitions set to none/0 "
        "and speaker notes cleared."
    )
