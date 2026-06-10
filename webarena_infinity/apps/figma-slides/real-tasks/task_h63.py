import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # In seed data, unresolved comments are on:
    # slide_003 (Q3 Highlights), slide_007 (Design System 2.0),
    # slide_013 (Competitive Landscape), slide_011 (Resource Allocation)
    expected_review_slides = {
        "slide_003": "Q3 Highlights [REVIEW]",
        "slide_007": "Design System 2.0 [REVIEW]",
        "slide_011": "Resource Allocation [REVIEW]",
        "slide_013": "Competitive Landscape [REVIEW]",
    }

    for s in state.get("slides", []):
        sid = s.get("id")
        if sid in expected_review_slides:
            expected_title = expected_review_slides[sid]
            actual_title = s.get("title", "")
            if actual_title != expected_title:
                errors.append(
                    f"Slide {sid} title is '{actual_title}', expected '{expected_title}'"
                )

    # All comments should be resolved
    for c in state.get("comments", []):
        if c.get("resolved") is not True:
            errors.append(
                f"Comment by {c.get('userName')} is not resolved"
            )

    if errors:
        return False, "; ".join(errors)
    return True, "Slides with unresolved comments marked [REVIEW]; all comments resolved"
