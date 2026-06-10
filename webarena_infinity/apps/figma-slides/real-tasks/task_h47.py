import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Slides with animated objects → easing should be ease_in_out
    # Slides with no animated objects → transition type should be none
    slides_with_animation = {
        "Q4 2025 Product Strategy", "Agenda", "Q3 Highlights",
        "Customer Feedback", "Q4 Roadmap", "Design System 2.0",
        "API Reference", "Data Comparison", "Resource Allocation",
        "Thank You"
    }
    slides_without_animation = {
        "Growth Metrics", "Team Survey Results", "Sprint Timeline",
        "Competitive Landscape", "Key Risks & Mitigations", "Next Steps"
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        trans = s.get("transition", {})

        if title in slides_with_animation:
            if trans.get("easing") != "ease_in_out":
                errors.append(
                    f"'{title}' easing is '{trans.get('easing')}', expected 'ease_in_out'"
                )

        elif title in slides_without_animation:
            if trans.get("type") != "none":
                errors.append(
                    f"'{title}' transition type is '{trans.get('type')}', expected 'none'"
                )

    if errors:
        return False, "; ".join(errors)
    return True, "Animated slides: ease_in_out easing; non-animated slides: transition none"
