import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    slides = state.get("slides", [])
    if not slides:
        return False, "No slides found in state"

    # Check that NO slide has dissolve transition
    dissolve_slides = []
    for s in slides:
        transition = s.get("transition", {})
        if transition.get("type") == "dissolve":
            dissolve_slides.append(s.get("title", s.get("id", "unknown")))

    if dissolve_slides:
        errors.append(f"Slides still using dissolve transition: {', '.join(dissolve_slides)}")

    # The slides that originally had dissolve should now have push with direction left
    # Original dissolve slides by title: Agenda, Customer Feedback, API Reference,
    # Team Survey Results, Data Comparison, Competitive Landscape, Next Steps, Thank You
    dissolve_titles = [
        "Agenda", "Customer Feedback", "API Reference",
        "Team Survey Results", "Data Comparison", "Competitive Landscape",
        "Next Steps", "Thank You"
    ]

    for s in slides:
        title = s.get("title", "")
        if title in dissolve_titles:
            transition = s.get("transition", {})
            t_type = transition.get("type", "")
            t_direction = transition.get("direction", "")
            if t_type != "push":
                errors.append(f"Slide '{title}' transition type is '{t_type}', expected 'push'")
            if t_direction != "left":
                errors.append(f"Slide '{title}' transition direction is '{t_direction}', expected 'left'")

    if errors:
        return False, "; ".join(errors)
    return True, "All dissolve transitions replaced with push-left successfully"
