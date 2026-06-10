import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # In seed data, these slides use dissolve transitions (should become slide_in, right)
    dissolve_titles = {
        "Agenda", "Customer Feedback", "API Reference",
        "Team Survey Results", "Data Comparison", "Competitive Landscape",
        "Next Steps", "Thank You"
    }
    # In seed data, these slides use push transitions (should get spring easing, 600ms)
    push_titles = {"Q3 Highlights", "Q4 Roadmap"}

    for s in state.get("slides", []):
        title = s.get("title", "")
        trans = s.get("transition", {})

        if title in dissolve_titles:
            if trans.get("type") != "slide_in":
                errors.append(f"'{title}' transition type is '{trans.get('type')}', expected 'slide_in'")
            if trans.get("direction") != "right":
                errors.append(f"'{title}' transition direction is '{trans.get('direction')}', expected 'right'")

        elif title in push_titles:
            if trans.get("type") != "push":
                errors.append(f"'{title}' should still be push, got '{trans.get('type')}'")
            if trans.get("easing") != "spring":
                errors.append(f"'{title}' easing is '{trans.get('easing')}', expected 'spring'")
            if trans.get("duration") != 600:
                errors.append(f"'{title}' duration is {trans.get('duration')}, expected 600")

    if errors:
        return False, "; ".join(errors)
    return True, "All dissolve transitions changed to slide_in right; push transitions updated to spring easing 600ms"
