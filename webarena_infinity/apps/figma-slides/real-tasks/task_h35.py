import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    # Ungrouped slides (groupId is null) in seed data:
    # Q4 2025 Product Strategy, Agenda, Competitive Landscape,
    # Key Risks & Mitigations, Next Steps, Thank You
    ungrouped_titles = {
        "Q4 2025 Product Strategy", "Agenda", "Competitive Landscape",
        "Key Risks & Mitigations", "Next Steps", "Thank You"
    }

    for s in state.get("slides", []):
        title = s.get("title", "")
        if title in ungrouped_titles:
            # Check background is gradient with correct colors
            bg = s.get("background", {})
            if bg.get("type") != "gradient":
                errors.append(f"'{title}' background type is '{bg.get('type')}', expected 'gradient'")
            else:
                gradient = bg.get("gradient", {})
                stops = gradient.get("stops", [])
                colors = [stop.get("color", "").upper() for stop in stops]
                if "#1E1E1E" not in colors:
                    errors.append(f"'{title}' gradient missing #1E1E1E")
                if "#2D1B69" not in colors:
                    errors.append(f"'{title}' gradient missing #2D1B69")

            # Check transition is dissolve with 500ms
            trans = s.get("transition", {})
            if trans.get("type") != "dissolve":
                errors.append(f"'{title}' transition type is '{trans.get('type')}', expected 'dissolve'")
            if trans.get("duration") != 500:
                errors.append(f"'{title}' transition duration is {trans.get('duration')}, expected 500")

    if errors:
        return False, "; ".join(errors)
    return True, "All ungrouped slides: gradient #1E1E1E->#2D1B69 background, dissolve 500ms transition"
