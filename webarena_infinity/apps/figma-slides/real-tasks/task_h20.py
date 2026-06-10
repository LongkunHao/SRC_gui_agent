import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Check no slide with title "Sprint Timeline"
    slides = state.get("slides", [])
    for s in slides:
        if s.get("title") == "Sprint Timeline":
            errors.append("Slide 'Sprint Timeline' should have been deleted but still exists")
            break

    # All comments should be resolved
    comments = state.get("comments", [])
    for c in comments:
        comment_id = c.get("id", "unknown")
        if c.get("resolved") is not True:
            errors.append(f"Comment {comment_id} has resolved={c.get('resolved')}, expected True")

    # Check share settings
    share = state.get("shareSettings", state.get("deckSettings", {}).get("shareSettings", {}))
    if not share:
        deck = state.get("deckSettings", {})
        share = deck.get("shareSettings", {})

    link_access = share.get("linkAccess", "")
    if link_access != "restricted":
        errors.append(f"linkAccess is '{link_access}', expected 'restricted'")

    link_role = share.get("linkRole", "")
    if link_role != "can_view":
        errors.append(f"linkRole is '{link_role}', expected 'can_view'")

    if errors:
        return False, "; ".join(errors)
    return True, "Sprint Timeline deleted, all comments resolved, link sharing restricted with view-only"
