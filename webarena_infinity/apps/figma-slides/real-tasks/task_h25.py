import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Determine which slides have unresolved comments
    slides_with_unresolved = set()
    for c in state.get("comments", []):
        if c.get("resolved") is not True:
            slides_with_unresolved.add(c.get("slideId"))

    # In seed data, unresolved comments are on:
    # slide_003 (Q3 Highlights), slide_007 (Design System 2.0),
    # slide_013 (Competitive Landscape), slide_011 (Resource Allocation)
    # These slides should now be skipped
    expected_skipped_titles = {
        "Q3 Highlights", "Design System 2.0",
        "Competitive Landscape", "Resource Allocation"
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in expected_skipped_titles:
            if s.get("skipped") is not True:
                errors.append(f"Slide '{title}' should be skipped (has unresolved comment)")

    # Check link access is restricted
    share = state.get("deckSettings", {}).get("shareSettings", {})
    link_access = share.get("linkAccess")
    if link_access != "restricted":
        errors.append(f"Link access is '{link_access}', expected 'restricted'")

    if errors:
        return False, "; ".join(errors)
    return True, "Slides with unresolved comments are skipped; link access set to restricted"
